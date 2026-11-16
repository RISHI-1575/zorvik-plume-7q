#!/usr/bin/env python
"""End-to-end checks for Saarathi Studio, through the same HTTP API the page uses.

    python e2e_studio.py                       # everything (~150 simulation runs)
    python e2e_studio.py --only api,upload     # pick phases: unit api gui upload sim same build download

Starts its own Studio server with a throwaway run folder, so Past runs are untouched.
Results CSVs and tripinfo files it adds under experiments/results are removed afterwards,
and every scenario / controller it creates is prefixed e2e_ and deleted at the end.
"""
import argparse
import csv
import io
import json
import math
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import studio  # noqa: E402

BUILT = ['program', 'fixed', 'actuated', 'maxp']
RES = ROOT / 'experiments' / 'results'
TALLY = {}            # phase -> [passed, failed]
FAILS = []


def check(phase, name, ok, detail=''):
    t = TALLY.setdefault(phase, [0, 0])
    t[0 if ok else 1] += 1
    if not ok:
        FAILS.append(f'[{phase}] {name}: {detail}')
        print(f'  FAIL [{phase}] {name}: {str(detail)[:300]}', flush=True)
    return ok


def http(path, body=None, raw=None):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    req = urllib.request.Request(BASE + path, data=data, method='GET' if data is None else 'POST',
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:          # dropped connection = server bug
        return 0, str(e).encode()


def J(b):
    try:
        return json.loads(b)
    except Exception:
        return None


def alive(phase, after):
    st, _ = http('/api/presets')
    check(phase, f'server alive after {after}', st == 200, st)


# ---------------------------------------------------------------- phases
def p_unit():
    r = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-q'],
                       cwd=ROOT, capture_output=True, text=True)
    check('unit', 'existing unit tests', r.returncode == 0, r.stderr[-800:])


def p_api():
    ph = 'api'
    scen = None
    for i in range(50):                       # every read endpoint, 50 times, stable answers
        st, b = http('/')
        check(ph, 'GET /', st == 200 and b'Saarathi Studio' in b, st)
        st, b = http('/api/presets')
        ps = J(b) or []
        check(ph, 'presets', st == 200 and len(ps) == 8 and all(
            len(p['bbox']) == 4 and p['bbox'][0] < p['bbox'][2] and p['bbox'][1] < p['bbox'][3]
            and studio.D > 0 and 12.7 < p['bbox'][0] < 13.2 and 77.4 < p['bbox'][1] < 77.9 for p in ps), st)
        st, b = http('/api/scenarios')
        s = J(b) or []
        check(ph, 'scenarios', st == 200 and len(s) >= 1 and all(
            (studio.SCEN / x['id'] / 'corridor.sumocfg').exists()
            and (not x['hourly_profile'] or len(x['hourly_profile']) == 24) for x in s), st)
        if scen is None:
            scen = [x['id'] for x in s]
        check(ph, 'scenario list stable', [x['id'] for x in s] == scen, [x['id'] for x in s])
        st, b = http('/api/controllers')
        cs = J(b) or []
        check(ph, 'controllers', st == 200 and [c['id'] for c in cs[:4]] == BUILT, st)
        st, b = http('/api/history')
        check(ph, 'history', st == 200 and isinstance(J(b), list), st)
    for i in range(max(50, 10 * len(scen))):  # road network of every built place
        sid = scen[i % len(scen)]
        st, b = http(f'/api/network/{sid}')
        g = J(b) or {}
        f = g.get('features', [])
        roads = [x for x in f if x['properties']['kind'] == 'road']
        sig = [x for x in f if x['properties']['kind'] == 'signal']
        pts = [c for x in roads for c in x['geometry']['coordinates']]
        check(ph, f'network {sid}', st == 200 and roads and sig and all(
            76.5 < lo < 78.5 and 12 < la < 14 for lo, la in pts), f'{st} roads={len(roads)} signals={len(sig)}')
    bad_get = ['/api/nope', '/api/result/zzz', '/api/result/abc123', '/api/result/..%2f..%2fetc',
               '/api/result', '/api/csv', '/api/csv/zzz', '/api/csv/abc123', '/api/csv/../../studio.py',
               '/api/replay/x', '/api/replay/abc.fixed', '/api/replay/abc.FIXED', '/api/replay/../x',
               '/api/replay', '/api/network/NOPE', '/api/network/nope', '/api/network/..', '/api/network',
               '/api/network/area_mwb5djg8x', '/api/job/nope', '/api/job', '/api/job/../../x', '/x', '/api',
               '/api/presets/../../etc/passwd', '/index.htm', '/studio.py', '/../studio.py']
    bad_get += [f'/api/result/{"a" * n}' for n in (1, 10, 40, 200)] + [f'/api/job/{n}' for n in range(20)]
    for p in bad_get:                          # never a 500 / dropped connection, never a file leak
        st, b = http(p)
        check(ph, f'GET {p}', (st in (400, 404) or p.startswith('/api/presets/')) and b'import ' not in b and b'root:' not in b, f'{st} {b[:120]}')
    alive(ph, 'bad GETs')

    good = {'scenario': 'silk_board', 'hour': 9, 'seeds': 1, 'demand': 0.6}
    bad_run = [{}, {'scenario': ''}, {'scenario': 'NOPE'}, {'scenario': '../silk_board'}, {'scenario': 'silk board'},
               {'scenario': None}, {'scenario': 5}, {'scenario': ['silk_board']}, {'scenario': 'area_mwb5djg8x'}]
    for k, vals in {'hour': [-1, 24, 99, 'x', None, [], {}, 'nine'],
                    'seeds': [0, 11, -3, 'x', None, 1e9],
                    'demand': [0, 0.01, 2.01, 5, -1, 'x', None, 'NaN', [], 1e308],
                    'controllers': [['nope'], ['fixed', 'nope'], 'fixed', [None], [''], ['../../x.py:X'], [1]],
                    'profile': ['nope', '../x']}.items():
        bad_run += [good | {k: v} for v in vals]
    for b in bad_run:                          # validation errors come back as 400 with a message, before any SUMO
        st, r = http('/api/run', b)
        if b.get('profile'):                   # profile is only checked by the run itself
            j = J(r) or {}
            if st == 200:
                job = wait(j['job_id'])
                check(ph, f'run {b}', job['status'] == 'error' and job['error'], job.get('status'))
                continue
        check(ph, f'run {b}', st == 400 and 'error' in (J(r) or {}), f'{st} {r[:150]}')
    for raw in [b'not json', b'{', b'[]', b'null', b'"x"', b'123', b'{"scenario": }', b'\xff\xfe']:
        st, r = http('/api/run', raw=raw)
        check(ph, f'run raw {raw!r}', st == 400, f'{st} {r[:120]}')
    st, r = http('/api/run', raw=b'{"a":"' + b'x' * 1_100_000 + b'"}')
    check(ph, 'oversized body refused', st in (0, 413), st)
    alive(ph, 'bad POSTs')


def wait(jid, timeout=1800):
    t0 = time.time()
    while time.time() - t0 < timeout:
        st, b = http(f'/api/job/{jid}')
        j = J(b) or {}
        if j.get('status') in ('done', 'error'):
            return j | {'secs': time.time() - t0}
        time.sleep(1)
    return {'status': 'timeout', 'error': f'over {timeout}s', 'secs': timeout}


def run_many(cfgs, cpu=18):
    """Submit runs, keeping about `cpu` SUMO processes busy; yield (cfg, job) as they finish."""
    pending, active = list(cfgs), {}
    while pending or active:
        while pending and (not active or sum(n for _, _, n in active.values())
                           + len(pending[0].get('controllers') or BUILT) * pending[0]['seeds'] <= cpu):
            c = pending.pop(0)
            st, b = http('/api/run', c)
            if st != 200:
                yield c, {'status': 'error', 'error': f'HTTP {st} {b[:200]}'}
                continue
            active[J(b)['job_id']] = (c, time.time(), len(c.get('controllers') or BUILT) * c['seeds'])
        time.sleep(1)
        for jid, (c, t0, _) in list(active.items()):
            j = J(http(f'/api/job/{jid}')[1]) or {}
            if j.get('status') in ('done', 'error') or time.time() - t0 > 1800:
                del active[jid]
                yield c, j | {'secs': time.time() - t0}


def fin(x):
    return isinstance(x, (int, float)) and math.isfinite(x)


def check_run(ph, c, job, keep_replay=False):
    tag = f"{c['scenario']} h{c['hour']} d{c['demand']} x{c['seeds']}{' ' + c['profile'] if c.get('profile') else ''}"
    if not check(ph, f'{tag} finished', job.get('status') == 'done', f"{job.get('status')} {job.get('error')}"):
        return None
    res = job['result']
    ctl = c.get('controllers') or BUILT
    tags = [x.split(':')[-1] for x in ctl]
    rows = res['rows']
    check(ph, f'{tag} rows', len(rows) == len(ctl) * c['seeds']
          and sorted({r['controller'] for r in rows}) == sorted(tags)
          and sorted({r['seed'] for r in rows}) == list(range(c['seeds'])), len(rows))
    for r in rows:
        nums = ['vehicles', 'delay_s', 'travel_time_s', 'waiting_s', 'stops_per_veh', 'collisions',
                'junction_collisions', 'teleports', 'emergency_stops', 'unfinished_vehicles', 'co2_kg', 'fuel_l',
                'delay_p95_s']
        check(ph, f"{tag} {r['controller']} s{r['seed']} numbers", all(fin(r.get(k)) and r[k] >= 0 for k in nums)
              and r['vehicles'] > 0 and r['travel_time_s'] >= r['delay_s'] - 1e-6
              and r['delay_p95_s'] >= r['delay_s'] * 0.5 and 0 <= r['bike_share'] <= 1,
              {k: r.get(k) for k in ('vehicles', 'delay_s', 'travel_time_s', 'delay_p95_s')})
    sm = {s['controller']: s for s in res['summary']}
    for t in tags:
        mine = [r['delay_s'] for r in rows if r['controller'] == t]
        check(ph, f'{tag} {t} summary', t in sm and sm[t]['n'] == c['seeds'] and mine
              and abs(sm[t]['delay_s']['mean'] - sum(mine) / len(mine)) < 1e-6, sm.get(t, {}).get('n'))
    st, b = http(f"/api/result/{res['run_id']}")
    check(ph, f'{tag} result saved', st == 200 and (J(b) or {}).get('run_id') == res['run_id'], st)
    st, b = http(res['csv_url'])
    cr = list(csv.DictReader(io.StringIO(b.decode()))) if st == 200 else []
    check(ph, f'{tag} csv', len(cr) == len(rows) and set(studio.COLS) <= set(cr[0] if cr else {}), len(cr))
    want = [x for x in ctl if ':' not in x]
    check(ph, f'{tag} replay list', sorted(res['replays']) == sorted(want), sorted(res['replays']))
    for k, u in res['replays'].items():
        st, b = http(u)
        rp = J(b) or {}
        fr, tls = rp.get('frames', []), rp.get('tls', [])
        check(ph, f'{tag} replay {k}', st == 200 and rp.get('roads') and tls and 0 < len(fr) <= 600
              and all(len(f['s']) == len(tls) and len(f['v']) % 5 == 0 for f in fr)
              and len(rp['series']['t']) == len(rp['series']['queue']) > 0, f'{st} frames={len(fr)}')
        if not keep_replay:
            (studio.RUNS / f"{res['run_id']}.{k}.replay.json").unlink(missing_ok=True)
    return res


def p_sim(scen):
    """Every built place at every hour (1 repeat), plus the UI's repeat counts and the API's limits."""
    ph = 'sim'
    dem = [0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.2]          # the page's traffic slider range
    cfgs = [{'scenario': s, 'hour': h, 'seeds': 1, 'demand': dem[(i + h) % len(dem)]}
            for i, s in enumerate(scen) for h in range(24)]
    cfgs += [{'scenario': s, 'hour': 9, 'seeds': n, 'demand': 0.6} for s in scen for n in (3, 5)]
    cfgs += [{'scenario': 'silk_board', 'hour': 18, 'seeds': 1, 'demand': d} for d in (0.05, 2.0)]
    cfgs += [{'scenario': 'corridor4', 'hour': 8, 'seeds': 10, 'demand': 0.6}]
    for s in studio.scenarios():
        cfgs += [{'scenario': s['id'], 'hour': 9, 'seeds': 1, 'demand': 0.6, 'profile': p} for p in s['profiles']]
    print(f'sim: {len(cfgs)} runs', flush=True)
    for i, (c, job) in enumerate(run_many(cfgs), 1):
        check_run(ph, c, job, keep_replay=i <= 2)
        print(f"  {i}/{len(cfgs)} {c['scenario']} h{c['hour']} x{c['seeds']} -> {job.get('status')} "
              f"{job.get('secs', 0):.0f}s", flush=True)
    st, b = http('/api/history')
    hist = J(b) or []
    check(ph, 'history lists every run, no blank entries', len(hist) >= len(cfgs) - 2
          and all(h.get('scenario') and h.get('run_id') for h in hist),
          [h for h in hist if not h.get('scenario')][:2])


def p_same():
    """Same settings, same numbers, including two identical runs started at the same moment."""
    ph = 'same'
    cfgs = [{'scenario': s, 'hour': h, 'seeds': 2, 'demand': 0.6}
            for s, h in [('silk_board', 9), ('silk_board', 18), ('domlur', 9), ('trinity', 13), ('corridor4', 8)]]
    for c in cfgs:
        a, b = (http('/api/run', c) for _ in range(2))      # concurrent twins
        ja, jb = wait(J(a[1])['job_id']), wait(J(b[1])['job_id'])
        jc = wait(J(http('/api/run', c)[1])['job_id'])      # and once more on its own
        rs = [check_run(ph, c, j) for j in (ja, jb, jc)]
        if all(rs):
            key = lambda res: sorted((r['controller'], r['seed'], r['vehicles'], round(r['delay_s'], 6))
                                     for r in res['rows'])
            check(ph, f"{c['scenario']} h{c['hour']} identical (twins + rerun)", key(rs[0]) == key(rs[1]) == key(rs[2]),
                  [key(r)[:2] for r in rs])


EXAMPLE = (ROOT / 'examples' / 'my_controller.py').read_text()
CRASH = '''class Boom:
    def __init__(self, tls_id):
        self.tls = tls_id
    def step(self, t, dt):
        if t > 30:
            raise RuntimeError('boom')
'''


def p_upload():
    ph = 'upload'
    made = []
    bad = [('e2e_a.py', 'x = 1', 'X'), ('e2e_a.py', 'class Y: pass', 'X'), ('e2e_a.py', 'class X: pass', ''),
           ('e2e_a.py', 'class X: pass', '1X'), ('e2e_a.py', 'class X: pass', 'X Y'), ('e2e_a.py', '', 'X'),
           ('e2e_a.py', 'class X: pass', 'X;import os'), ('e2e_a.py', '  class X: pass', 'X'),
           ('e2e_a.py', 'class XY: pass', 'X'), ('e2e_a.py', '#class X: pass', 'X'), ('e2e_a.py', 'class X: pass', '.*')]
    bad += [('e2e_a.py', 'class X: pass', n) for n in ('X-Y', 'X.Y', '$X', 'X\n', ' X', 'é?', '', '()', '[X]')]
    bad += [('e2e_a.py', f'class {n}: pass', 'Other') for n in ('A', 'B', 'C', 'Foo', 'Bar', 'Ctl', 'Q', 'R', 'S', 'T')]
    for fn, code, cls in bad:
        st, b = http('/api/controllers', {'filename': fn, 'code': code, 'class_name': cls})
        check(ph, f'reject {fn} {cls!r}', st == 400, f'{st} {b[:100]}')
    names = ['e2e_ok.py', 'E2E Mixed Case.py', '../../e2e_escape.py', 'e2e_dots.v2.py', 'e2e-dash.py',
             '/abs/e2e_abs.py', 'e2e_ünï.py', 'e2e_ok.txt', 'e2e_sp ace.py', 'e2e_' + 'x' * 60 + '.py']
    for i in range(30):
        fn = names[i % len(names)]
        st, b = http('/api/controllers', {'filename': fn, 'code': EXAMPLE, 'class_name': 'LongestQueue'})
        cid = (J(b) or {}).get('id', '')
        f = ROOT / cid.split(':')[0] if cid else None
        ok = st == 200 and f and f.resolve().parent == studio.USER.resolve() and f.exists()
        check(ph, f'accept {fn!r}', ok, f'{st} {b[:120]}')
        if ok:
            made.append(f)
            st, b = http('/api/controllers')
            check(ph, f'listed {cid}', cid in [c['id'] for c in J(b) or []], st)
    st, b = http('/api/controllers', {'filename': 'e2e_boom.py', 'code': CRASH, 'class_name': 'Boom'})
    boom = (J(b) or {}).get('id')
    made.append(ROOT / boom.split(':')[0])
    ok_id = 'user_controllers/e2e_ok.py:LongestQueue'
    for c, job in run_many([{'scenario': s, 'hour': 9, 'seeds': 1, 'demand': 0.6, 'controllers': ['maxp', ok_id]}
                            for s in ('silk_board', 'trinity', 'corridor4')]):
        check_run(ph, c, job)
    j = wait(J(http('/api/run', {'scenario': 'silk_board', 'hour': 9, 'seeds': 1, 'demand': 0.6,
                                 'controllers': ['fixed', boom]})[1])['job_id'])
    check(ph, 'crashing controller reports an error', j['status'] == 'error' and j.get('error'), j.get('status'))
    alive(ph, 'crashing controller')
    for f in set(made):
        f.unlink(missing_ok=True)


def p_gui():
    ph = 'gui'
    import os
    if sys.platform != 'darwin' or os.environ.get('DISPLAY'):
        return print('gui: skipped (a display is available; would open 50 windows)')
    for i in range(50):
        st, b = http('/api/gui', {'scenario': ['silk_board', 'domlur', 'trinity', 'corridor4', 'old_airport_road'][i % 5]})
        check(ph, 'gui explains XQuartz', st in (400, 500) and b'XQuartz' in b, f'{st} {b[:100]}')


def p_build(download):
    ph = 'download' if download else 'build'
    bad = [{}, {'name': 'x'}, {'name': 'X_bad', 'bbox': [12.9, 77.6, 12.91, 77.61]}, {'name': '1abc', 'bbox': [1, 2, 3, 4]},
           {'name': 'e2e_ok', 'bbox': [1, 2, 3]}, {'name': 'e2e_ok', 'bbox': 'x'}, {'name': 'e2e_ok', 'bbox': None},
           {'name': 'e2e_ok', 'bbox': [1, 2, 3, 4, 5]}, {'name': 'e2e_ok', 'bbox': ['a', 'b', 'c', 'd']},
           {'name': '../e2e', 'bbox': [12.9, 77.6, 12.91, 77.61]}, {'name': 'e2e ok', 'bbox': [12.9, 77.6, 12.91, 77.61]},
           {'name': 'e' * 60, 'bbox': [12.9, 77.6, 12.91, 77.61]}, {'name': None, 'bbox': [12.9, 77.6, 12.91, 77.61]},
           {'name': 'e2e_ok', 'bbox': [None, 1, 2, 3]}, {'name': 'e2e_ok', 'bbox': {}}]
    fail_jobs = [[12.91, 77.6, 12.90, 77.61], [12.9, 77.61, 12.91, 77.60], [12.9, 77.6, 12.9, 77.6],
                 [12.8, 77.5, 13.0, 77.7], [0, 0, 10, 10], [12.9, 77.6, 12.95, 77.66], [-90, -180, 90, 180],
                 ['nan', 77.6, 12.91, 77.61], [12.9, 'inf', 12.91, 77.61]]
    if not download:
        for b in bad:
            st, r = http('/api/build', b)
            check(ph, f'reject {b}', st == 400, f'{st} {r[:100]}')
        for i in range(50 - len(bad) - len(fail_jobs)):
            st, r = http('/api/build', {'name': f'E2E_{i}', 'bbox': [12.9, 77.6, 12.91, 77.61]})
            check(ph, f'reject name E2E_{i}', st == 400, st)
        for i, bb in enumerate(fail_jobs):     # pass the shape check, refused by the builder before any download
            st, r = http('/api/build', {'name': f'e2e_bad{i}', 'bbox': bb})
            j = wait(J(r)['job_id'], 120) if st == 200 else {'status': 'error', 'error': 'HTTP 400'}
            check(ph, f'builder refuses {bb}', j['status'] == 'error' and j.get('error'), j)
            check(ph, f'no folder for e2e_bad{i}', not (studio.SCEN / f'e2e_bad{i}' / 'corridor.yaml').exists(), '')
        # Real builds from already-downloaded OSM (no network): copy area.osm, rebuild under a new name.
        srcs = [s for s in studio.scenarios() if s['bbox'] and (studio.SCEN / s['id'] / 'area.osm').exists()]
        todo = [(f"e2e_{s['id']}", s['bbox'], studio.SCEN / s['id'] / 'area.osm') for s in srcs]
    else:
        built = {s['id'] for s in studio.scenarios()}
        todo = [(i, [la - studio.D, lo - studio.D, la + studio.D, lo + studio.D], None)
                for i, _, la, lo, _ in studio.PRESETS if i not in built]
    ready = []
    for name, bb, osm in todo:
        if osm:
            (studio.SCEN / name).mkdir(exist_ok=True)
            shutil.copy(osm, studio.SCEN / name / 'area.osm')
        st, r = http('/api/build', {'name': name, 'bbox': bb})
        j = wait(J(r)['job_id'], 900) if st == 200 else {'status': 'error', 'error': r}
        ok = check(ph, f'build {name}', j['status'] == 'done', j.get('error'))
        print(f"  build {name}: {j['status']} {j.get('secs', 0):.0f}s {j.get('error') or ''}", flush=True)
        if ok:
            st, b = http('/api/scenarios')
            check(ph, f'{name} listed', name in [s['id'] for s in J(b) or []], st)
            st, b = http(f'/api/network/{name}')
            check(ph, f'{name} network', st == 200 and len((J(b) or {}).get('features', [])) > 0, st)
            ready.append(name)
    for c, job in run_many([{'scenario': n, 'hour': h, 'seeds': 1, 'demand': 0.6} for n in ready for h in (9, 18)]):
        check_run(ph, c, job)


def main():
    global BASE
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='unit,api,gui,upload,sim,same,build,download')
    phases = ap.parse_args().only.split(',')

    studio.RUNS = Path(tempfile.mkdtemp(prefix='saarathi_e2e_'))
    before = {p: p.read_bytes() for p in RES.rglob('results_v5.csv')}
    files_before = set(RES.rglob('*'))
    scen_before = {p.name for p in studio.SCEN.iterdir()}
    srv = studio.HTTPServer(('127.0.0.1', 0), studio.H)
    BASE = f'http://127.0.0.1:{srv.server_port}'
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    t0 = time.time()
    try:
        scen = [s['id'] for s in studio.scenarios()]
        for p in phases:
            print(f'== {p}', flush=True)
            {'unit': p_unit, 'api': p_api, 'gui': p_gui, 'upload': p_upload, 'sim': lambda: p_sim(scen),
             'same': p_same, 'build': lambda: p_build(False), 'download': lambda: p_build(True)}[p]()
    finally:
        srv.shutdown()
        for p, data in before.items():                 # leave the real results exactly as they were
            p.write_bytes(data)
        for p in sorted(set(RES.rglob('*')) - files_before, reverse=True):
            p.unlink() if p.is_file() else p.rmdir()
        for name in {p.name for p in studio.SCEN.iterdir()} - scen_before:
            if name.startswith('e2e_'):
                shutil.rmtree(studio.SCEN / name)
        shutil.rmtree(studio.RUNS)
    print(f'\n{"phase":<10}{"passed":>8}{"failed":>8}')
    for p, (a, b) in TALLY.items():
        print(f'{p:<10}{a:>8}{b:>8}')
    print(f'total {sum(a for a, _ in TALLY.values())} passed, {len(FAILS)} failed, {time.time() - t0:.0f}s')
    for f in FAILS[:60]:
        print(' ', f)
    sys.exit(1 if FAILS else 0)


if __name__ == '__main__':
    main()
