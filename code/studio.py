#!/usr/bin/env python
"""Saarathi Studio: pick a Bengaluru area, plug in signal algorithms, compare.

    python studio.py            # then open http://127.0.0.1:8765

Local-only web UI (stdlib http.server). Builds and simulations run as
subprocesses of make_area.py / run.py, so the CLI and the Studio give
identical numbers. Uploaded controllers are executed as Python on this
machine: the server binds to 127.0.0.1 only.
"""
import csv
import datetime as dt
import json
import os
import re
import statistics
import subprocess
import sys
import threading
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
SCEN = ROOT / 'scenarios'
USER = ROOT / 'user_controllers'
RUNS = ROOT / 'experiments' / 'studio_runs'
ENV = {**os.environ, 'PATH': f'{Path(sys.executable).parent}{os.pathsep}{os.environ.get("PATH", "")}'}
sys.path.insert(0, str(ROOT))
from run import COLS  # noqa: E402  (pure list; run.py's config import is harmless here)

# Approximate boxes (~1.7 km2) around well-known Bengaluru junctions. S W N E.
PRESETS = [
    ('silk_board', 'Central Silk Board', 12.9177, 77.6238, 'Hosur Rd x ORR, flyover + metro; among the most congested junctions in the city'),
    ('hebbal', 'Hebbal flyover', 13.0358, 77.5970, 'Airport road x ORR interchange'),
    ('marathahalli', 'Marathahalli bridge', 12.9569, 77.7011, 'ORR x Old Airport Rd, IT corridor'),
    ('tin_factory', 'Tin Factory / KR Puram', 12.9967, 77.6680, 'Old Madras Rd x ORR approach'),
    ('domlur', 'Domlur flyover', 12.9610, 77.6387, 'Inner Ring Rd x Old Airport Rd (BTP cycle data exists for Domlur)'),
    ('iblur', 'Iblur / Agara', 12.9216, 77.6674, 'ORR x Sarjapur Rd'),
    ('trinity', 'Trinity circle / MG Road', 12.9730, 77.6190, 'CBD arterial, metro above'),
    ('mekhri', 'Mekhri circle', 13.0140, 77.5830, 'Bellary Rd underpass'),
]
D = 0.0065
BUILTINS = [
    ('program', 'Signal plan in the map', 'the stored plan; BTP-published cycle where known (Domlur, ISRO, Yamlur)'),
    ('fixed', 'Fixed-time', "today's typical signal: rotate greens on a fixed cycle"),
    ('actuated', 'Actuated (gap)', 'extends green while vehicles keep arriving'),
    ('maxp', 'Max-pressure (PCU)', 'serves the movement with most PCU-weighted pressure'),
]

JOBS, NETCACHE = {}, {}
EXTRA = ['delay_p95_s', 'co2_kg', 'fuel_l']   # row keys outside the versioned CSV schema


def scenarios():
    out = []
    for y in sorted(SCEN.glob('*/corridor.yaml')):
        if not (y.parent / 'corridor.sumocfg').exists():
            continue
        m = yaml.safe_load(y.read_text())
        net = m.get('network', {})
        out.append({'id': y.parent.name, 'name': m.get('name', y.parent.name),
                    'description': m.get('description', ''),
                    'signals': net.get('signals') or {}, 'bbox': net.get('bbox'),
                    'hourly_profile': m.get('traffic', {}).get('hourly_profile', []),
                    'profiles': list((m.get('behaviour') or {}).get('profiles') or {})})
    return out


def scenario_dir(sid):
    d = SCEN / sid
    if not re.fullmatch(r'[a-z0-9_]+', sid or '') or not (d / 'corridor.yaml').exists():
        raise ValueError(f'unknown scenario {sid!r}')
    return d


def network_geojson(sid):
    d = scenario_dir(sid)
    net_file = d / 'corridor.net.xml'
    key = (sid, net_file.stat().st_mtime)
    if key in NETCACHE:
        return NETCACHE[key]
    import sumolib
    net = sumolib.net.readNet(str(net_file))
    ll = lambda xy: [round(v, 6) for v in net.convertXY2LonLat(*xy)]
    if not net.hasGeoProj():   # synthetic corridor4: plain metres, no map
        ll = lambda xy: [77.6 + xy[0] / 1e5, 12.97 + xy[1] / 1.1e5]
    feats = [{'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [ll(p) for p in e.getShape()]},
              'properties': {'kind': 'road', 'lanes': e.getLaneNumber(), 'name': e.getName()}}
             for e in net.getEdges()]
    names = {str(v): k for k, v in (yaml.safe_load((d / 'corridor.yaml').read_text())
                                     .get('network', {}).get('signals') or {}).items()}
    for t in net.getTrafficLights():
        conns = t.getConnections()
        if conns:
            node = conns[0][0].getEdge().getToNode()
            feats.append({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': ll(node.getCoord())},
                          'properties': {'kind': 'signal', 'id': t.getID(), 'name': names.get(t.getID(), t.getID())}})
    NETCACHE[key] = g = {'type': 'FeatureCollection', 'features': feats}
    return g


def controllers():
    out = [{'id': k, 'name': n, 'builtin': True, 'description': desc} for k, n, desc in BUILTINS]
    for f in [ROOT / 'examples' / 'my_controller.py', *sorted(USER.glob('*.py'))]:
        for cls in re.findall(r'^class (\w+)', f.read_text(), re.M):
            out.append({'id': f'{f.relative_to(ROOT)}:{cls}', 'name': cls, 'builtin': False,
                        'description': f'{f.relative_to(ROOT)}'})
    return out


def start_job(kind, cmd, total, finish):
    jid = uuid.uuid4().hex[:10]
    job = JOBS[jid] = {'status': 'running', 'progress': 0.0, 'log': [], 'kind': kind,
                       'result': None, 'error': None}

    def work():
        p = subprocess.Popen(cmd, cwd=ROOT, env=ENV, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True, bufsize=1)
        done = 0
        for line in p.stdout:
            line = line.rstrip()
            if 'Retrying in' in line or not line:
                continue
            job['log'].append(line)
            if line.startswith('done ') or line.startswith(('osm:', 'net:', 'signals:', 'ready:')):
                done += 1
                job['progress'] = min(0.99, done / total)
        if p.wait() != 0:
            job['status'], job['error'] = 'error', (job['log'][-1] if job['log'] else 'failed')
            return
        try:
            job['result'] = finish()
            job['status'], job['progress'] = 'done', 1.0
        except Exception as e:   # surface to the UI, never kill the server
            job['status'], job['error'] = 'error', str(e)
    threading.Thread(target=work, daemon=True).start()
    return jid


def summarise(rows):
    by = {}
    for r in rows:
        by.setdefault(r['controller'], []).append(r)
    out = []
    for c, rs in by.items():
        s = {'controller': c, 'n': len(rs)}
        for k in COLS + EXTRA:
            v = [float(r[k]) for r in rs if r.get(k) is not None]
            if v:
                s[k] = {'mean': statistics.fmean(v), 'std': statistics.stdev(v) if len(v) > 1 else 0.0}
        out.append(s)
    return out


def api_run(b):
    sid = scenario_dir(b['scenario']).name
    ctl = [str(c) for c in b.get('controllers') or [k for k, *_ in BUILTINS]]
    known = {c['id'] for c in controllers()}
    if not ctl or not set(ctl) <= known:
        raise ValueError('choose controllers from /api/controllers')
    hour, seeds, dem = int(b.get('hour', 9)), int(b.get('seeds', 3)), float(b.get('demand', 0.6))
    if not (0 <= hour <= 23 and 1 <= seeds <= 10 and 0.05 <= dem <= 2.0):
        raise ValueError('hour 0-23, seeds 1-10, demand 0.05-2.0')
    run_id = dt.datetime.now().strftime('%Y%m%d-%H%M%S-') + uuid.uuid4().hex[:4]
    RUNS.mkdir(parents=True, exist_ok=True)
    rows_file = RUNS / f'{run_id}.rows.json'
    cmd = [sys.executable, '-u', 'run.py', '--scenario', str(SCEN / sid / 'corridor.yaml'), '--compare',
           '--controllers', ','.join(ctl), '--seeds', str(seeds), '--hours', str(hour), str(hour + 1),
           '--demand', str(dem), '--jobs', str(min(len(ctl) * seeds, os.cpu_count() or 2)),
           '--json', str(rows_file), '--replay', str(RUNS / run_id)]
    if b.get('profile'):
        cmd += ['--profile', str(b['profile'])]

    def finish():
        rows = json.loads(rows_file.read_text())
        rows_file.unlink()
        with (RUNS / f'{run_id}.csv').open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['scenario', 'profile', 'hours', 'demand', 'controller', 'seed'] + COLS,
                               extrasaction='ignore')
            w.writeheader()
            w.writerows(rows)
        res = {'run_id': run_id, 'created': dt.datetime.now().isoformat(timespec='seconds'),
               'scenario': sid, 'hour': hour, 'demand': dem, 'profile': b.get('profile') or 'active',
               'controllers': ctl, 'csv_url': f'/api/csv/{run_id}', 'rows': rows, 'summary': summarise(rows),
               'replays': {c: f'/api/replay/{run_id}.{c}' for c in ctl
                           if (RUNS / f'{run_id}.{c}.replay.json').exists()}}
        (RUNS / f'{run_id}.json').write_text(json.dumps(res))
        return res
    return {'job_id': start_job('run', cmd, len(ctl) * seeds, finish)}


def api_build(b):
    name, bbox = str(b.get('name', '')), b.get('bbox')
    if not re.fullmatch(r'[a-z][a-z0-9_]{1,40}', name) or not (isinstance(bbox, list) and len(bbox) == 4):
        raise ValueError('name must be a lowercase slug and bbox [s, w, n, e]')
    cmd = [sys.executable, '-u', 'scenarios/make_area.py', '--name', name, '--bbox', *map(str, map(float, bbox))]
    return {'job_id': start_job('build', cmd, 4, lambda: {'scenario': name})}


def api_upload(b):
    fn, code, cls = str(b.get('filename', '')), str(b.get('code', '')), str(b.get('class_name', ''))
    stem = re.sub(r'[^a-z0-9_]', '_', Path(fn).stem.lower()) or 'controller'
    if not re.fullmatch(r'[A-Za-z_]\w*', cls) or not re.search(rf'^class {cls}\b', code, re.M):
        raise ValueError(f'class {cls!r} not found in {fn}')
    USER.mkdir(exist_ok=True)
    (USER / f'{stem}.py').write_text(code)
    return {'id': f'user_controllers/{stem}.py:{cls}'}


def api_gui(b):
    sid = scenario_dir(b['scenario']).name
    hour, dem = int(b.get('hour', 9)), float(b.get('demand', 0.6))
    # The pip sumo-gui on macOS draws through X11; without XQuartz it dies with "unable to open display".
    if sys.platform == 'darwin' and not os.environ.get('DISPLAY'):
        raise RuntimeError('sumo-gui needs XQuartz on macOS: brew install --cask xquartz, '
                           'log out and back in, then restart the Studio.')
    RUNS.mkdir(parents=True, exist_ok=True)
    with (RUNS / 'gui.log').open('w') as f:  # read this if the window never appears
        subprocess.Popen([sys.executable, 'run.py', '--scenario', str(SCEN / sid / 'corridor.yaml'),
                          '--controller', str(b.get('controller') or 'fixed'), '--hours', str(hour), str(hour + 1),
                          '--demand', str(dem), '--gui'], cwd=ROOT, env=ENV,
                         stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
    return {'ok': True, 'log': str(RUNS / 'gui.log')}


def history():
    out = []
    for f in sorted(RUNS.glob('*.json')):
        if f.name.endswith(('.rows.json', '.replay.json')):
            continue
        r = json.loads(f.read_text())
        out.append({k: r.get(k) for k in ('run_id', 'created', 'scenario', 'hour', 'demand', 'controllers', 'replays')})
    return out


def run_file(run_id, ext):
    if not re.fullmatch(r'[0-9a-f-]+', run_id):
        raise ValueError('bad run id')
    return RUNS / f'{run_id}.{ext}'


GET = {
    'presets': lambda _: [{'id': i, 'name': n, 'bbox': [la - D, lo - D, la + D, lo + D], 'note': note}
                          for i, n, la, lo, note in PRESETS],
    'scenarios': lambda _: scenarios(),
    'network': network_geojson,
    'controllers': lambda _: controllers(),
    'job': lambda jid: JOBS.get(jid) or (_ for _ in ()).throw(ValueError('no such job')),
    'history': lambda _: history(),
    'result': lambda rid: json.loads(run_file(rid, 'json').read_text()),
}
POST = {'build': api_build, 'run': api_run, 'controllers': api_upload, 'gui': api_gui}


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype='application/json', extra=None):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _route(self, table, arg_fn):
        parts = self.path.split('?')[0].strip('/').split('/')
        if self.path in ('/', '/index.html'):
            return self._send(200, (ROOT / 'studio' / 'index.html').read_bytes(), 'text/html; charset=utf-8')
        if len(parts) >= 2 and parts[0] == 'api' and parts[1] == 'csv' and table is GET:
            f = run_file(parts[2], 'csv')
            return self._send(200, f.read_bytes(), 'text/csv',
                              {'Content-Disposition': f'attachment; filename="saarathi_{parts[2]}.csv"'})
        if len(parts) == 3 and parts[:2] == ['api', 'replay'] and table is GET:
            if not re.fullmatch(r'[0-9a-f-]+\.[a-z0-9_]+', parts[2]):
                raise ValueError('bad replay id')
            return self._send(200, (RUNS / f'{parts[2]}.replay.json').read_bytes())
        if len(parts) < 2 or parts[0] != 'api' or parts[1] not in table:
            return self._send(404, {'error': 'not found'})
        self._send(200, table[parts[1]](arg_fn(parts)))

    def _safe(self, table, arg_fn):
        try:
            self._route(table, arg_fn)
        except (ValueError, KeyError, TypeError, IndexError, FileNotFoundError) as e:   # bad input
            self._send(400, {'error': str(e)})
        except Exception as e:
            self._send(500, {'error': f'{type(e).__name__}: {e}'})

    def do_GET(self):
        self._safe(GET, lambda p: p[2] if len(p) > 2 else None)

    def do_POST(self):
        n = int(self.headers.get('Content-Length', 0))
        if n > 1_000_000:
            return self._send(413, {'error': 'body too large'})
        raw = self.rfile.read(n)

        def body(_):
            b = json.loads(raw or b'{}')
            if not isinstance(b, dict):
                raise ValueError('body must be a JSON object')
            return b
        self._safe(POST, body)

    def log_message(self, *a):
        pass


if __name__ == '__main__':
    port = int(os.environ.get('SAARATHI_PORT', 8765))
    print(f'Saarathi Studio: http://127.0.0.1:{port}', flush=True)
    HTTPServer(('127.0.0.1', port), H).serve_forever()
