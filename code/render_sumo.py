"""Headless top-down render of any Saarathi scenario (real SUMO state via TraCI).

  python render_sumo.py --scenario scenarios/old_airport_road/corridor.yaml --focus isro
  python render_sumo.py --scenario scenarios/corridor4/corridor.yaml --focus J2

Writes overview.png (whole corridor, OSM buildings if present) and
<focus>_closeup.gif (stop-line view: two-wheelers filtering) to --out.
"""
import argparse, math, os, sys, tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--scenario', required=True)
ap.add_argument('--focus', help='signal name from the manifest, or a node id')
ap.add_argument('--out', default='experiments/renders')
ap.add_argument('--hour', type=int, default=8)
ap.add_argument('--warmup', type=int, default=1200, help='seconds before frames')
ap.add_argument('--frames', type=int, default=60)
ap.add_argument('--radius', type=float, default=70, help='close-up half-width (m)')
args = ap.parse_args()
os.environ['SAARATHI_SCENARIO'] = str(Path(args.scenario).resolve())
sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection
import sumolib, traci
from saarathi import demand
from saarathi.config import SCENARIO, SCENARIO_DIR

BG, ROAD, BLD, FG = '#0b0f14', '#465062', '#1b212b', '#c9d1d9'
COL = {'bike': '#ff922b', 'auto': '#51cf66', 'car': '#4dabf7', 'lcv': '#b197fc',
       'bus': '#f06595', 'truck': '#ced4da'}
TL = {'r': '#ff4d4f', 's': '#ff4d4f', 'y': '#fcc419', 'u': '#fcc419',
      'g': '#40c057', 'G': '#40c057'}
out = Path(args.out) / SCENARIO_DIR.name
out.mkdir(parents=True, exist_ok=True)
net = sumolib.net.readNet(str(SCENARIO_DIR / 'corridor.net.xml'), withInternal=True)
lanes = [(ln.getShape(), ln.getWidth()) for e in net.getEdges(withInternal=True)
         for ln in e.getLanes()]
buildings = []
poly_file = SCENARIO_DIR / 'buildings.poly.xml'
if poly_file.exists():
    for p in ET.parse(poly_file).getroot().iter('poly'):
        if 'building' in p.get('type', ''):
            buildings.append([tuple(map(float, xy.split(','))) for xy in p.get('shape').split()])

signals = SCENARIO.network.get('signals', {})
focus = signals.get(args.focus, args.focus) or SCENARIO.junction_ids[0]
if net.hasNode(focus):
    cx, cy = net.getNode(focus).getCoord()
else:  # joined TLS cluster: centre of its stop lines
    ends = [c[0].getShape()[-1] for c in net.getTLS(focus).getConnections()]
    cx, cy = (sum(p[i] for p in ends) / len(ends) for i in (0, 1))


def figure(xlim, ylim, width_in):
    h = width_in * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
    fig = plt.figure(figsize=(width_in, max(h, 2.0)), dpi=130, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect('equal'); ax.axis('off')
    ppm = width_in * 72 / (xlim[1] - xlim[0])          # points per metre
    if buildings:
        ax.add_collection(PolyCollection(buildings, facecolor=BLD, edgecolor='#222a35', lw=0.3, zorder=1))
    ax.add_collection(LineCollection([s for s, _ in lanes], colors=ROAD,
                                     linewidths=[max(w * ppm, 1.0) for _, w in lanes],
                                     capstyle='butt', zorder=2))
    return fig, ax


def dynamic(ax, mark=3, dots=0):
    arts = []
    for tls in traci.trafficlight.getIDList():
        state = traci.trafficlight.getRedYellowGreenState(tls)
        pts = {}
        for i, links in enumerate(traci.trafficlight.getControlledLinks(tls)):
            if links and i < len(state):
                pts[net.getLane(links[0][0]).getShape()[-1]] = TL.get(state[i], '#868e96')
        if pts:
            xs, ys = zip(*pts)
            arts.append(ax.scatter(xs, ys, s=mark, c=list(pts.values()), marker='s', zorder=4, lw=0))
    bodies, colors = [], []
    if dots:  # overview: a vehicle is sub-pixel, draw a dot
        ids = traci.vehicle.getIDList()
        xy = [traci.vehicle.getPosition(v) for v in ids]
        if xy:
            arts.append(ax.scatter(*zip(*xy), s=dots, lw=0, zorder=5,
                                   c=[COL.get(traci.vehicle.getTypeID(v), '#fff') for v in ids]))
        return arts
    for v in traci.vehicle.getIDList():
        x, y = traci.vehicle.getPosition(v)
        a = math.radians(90 - traci.vehicle.getAngle(v))
        L, W = traci.vehicle.getLength(v), traci.vehicle.getWidth(v)
        dx, dy, nx, ny = math.cos(a), math.sin(a), -math.sin(a) * W / 2, math.cos(a) * W / 2
        bx, by = x - dx * L, y - dy * L
        bodies.append([(x + nx, y + ny), (x - nx, y - ny), (bx - nx, by - ny), (bx + nx, by + ny)])
        colors.append(COL.get(traci.vehicle.getTypeID(v), '#fff'))
    arts.append(ax.add_collection(PolyCollection(bodies, facecolors=colors, lw=0, zorder=5)))
    return arts


def caption(ax, text):
    t = ax.text(0.01, 0.98, text, transform=ax.transAxes, color=FG, fontsize=9,
                va='top', family='monospace', zorder=6)
    keys = ax.legend(handles=[plt.Line2D([], [], ls='', marker='s', color=c, label=k)
                              for k, c in COL.items()], loc='lower right', ncol=6,
                     fontsize=7, frameon=False, labelcolor=FG)
    return [t]


with tempfile.TemporaryDirectory() as tmp:
    routes = demand.generate(hours=(args.hour, args.hour + 1), seed=42,
                             out=Path(tmp) / 'routes.rou.xml')
    traci.start(['sumo', '-c', str(SCENARIO_DIR / 'corridor.sumocfg'), '-r', str(routes),
                 '--seed', '42', '--no-warnings', 'true'])
    for _ in range(args.warmup):
        traci.simulationStep()
    head = f'{SCENARIO.name} | {args.hour:02d}:00 + {args.warmup // 60} min'

    (x0, y0), (x1, y1) = net.getBBoxXY()
    if buildings:  # crop to the built-up corridor, not the network's long tails
        ys = [y for b in buildings for _, y in b]
        y0, y1 = min(ys) - 150, max(ys) + 150
    fig, ax = figure((x0, x1), (y0, y1), 16)
    dynamic(ax, mark=10, dots=4)
    caption(ax, f'{head} | {traci.vehicle.getIDCount()} vehicles | live SUMO state\n'
                f'Map data (c) OpenStreetMap contributors' if buildings else head)
    fig.savefig(out / 'overview.png', facecolor=BG); plt.close(fig)

    r = args.radius
    fig, ax = figure((cx - r, cx + r), (cy - r * 0.62, cy + r * 0.62), 9)
    caption(ax, '')
    frames = []
    from PIL import Image
    for k in range(args.frames):
        traci.simulationStep()
        arts = dynamic(ax, mark=40)
        arts.append(ax.text(0.01, 0.98, f'{head} | {args.focus or focus} | t+{k}s\n'
                            'sublane 0.4 m: two-wheelers filter to the stop line',
                            transform=ax.transAxes, color=FG, fontsize=9, va='top',
                            family='monospace', zorder=6))
        fig.canvas.draw()
        frames.append(Image.frombytes('RGBA', fig.canvas.get_width_height(),
                                      bytes(fig.canvas.buffer_rgba())).convert('RGB'))
        if k == 0:
            fig.savefig(out / f'{args.focus or "focus"}_closeup.png', facecolor=BG)
        for a in arts:
            a.remove()
    traci.close()
frames[0].save(out / f'{args.focus or "focus"}_closeup.gif', save_all=True,
               append_images=frames[1:], duration=150, loop=0)
print('wrote', *sorted(p.name for p in out.iterdir()))
