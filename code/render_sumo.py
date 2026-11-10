"""Headless SUMO render: run the real corridor4 scenario via TraCI and draw top-down frames."""
import math, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import sumolib, traci

SCN, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
net = sumolib.net.readNet(os.path.join(SCN, "corridor.net.xml"), withInternal=True)
COL = {"bike": "#e8590c", "auto": "#2f9e44", "car": "#1c7ed6", "lcv": "#7048e8", "bus": "#c2255c", "truck": "#495057"}
TL = {"r": "#e03131", "y": "#f59f00", "g": "#2f9e44", "G": "#2f9e44", "s": "#e03131", "u": "#f59f00", "o": "#adb5bd", "O": "#adb5bd"}

def draw_net(ax):
    for e in net.getEdges(withInternal=True):
        for ln in e.getLanes():
            xs, ys = zip(*ln.getShape())
            ax.plot(xs, ys, color="#dee2e6", lw=ln.getWidth() * PX, solid_capstyle="butt", zorder=1)

def draw_frame(ax, title):
    for tls in traci.trafficlight.getIDList():
        state = traci.trafficlight.getRedYellowGreenState(tls)
        for i, links in enumerate(traci.trafficlight.getControlledLinks(tls)):
            if not links or i >= len(state):
                continue
            x, y = net.getLane(links[0][0]).getShape()[-1]
            ax.plot(x, y, "s", ms=3, color=TL.get(state[i], "#000"), zorder=3)
    for v in traci.vehicle.getIDList():
        x, y = traci.vehicle.getPosition(v)
        a = math.radians(90 - traci.vehicle.getAngle(v))
        L, W = traci.vehicle.getLength(v), traci.vehicle.getWidth(v)
        dx, dy = math.cos(a), math.sin(a)  # front is (x,y); body extends backwards
        nx, ny = -dy * W / 2, dx * W / 2
        bx, by = x - dx * L, y - dy * L
        poly = [(x + nx, y + ny), (x - nx, y - ny), (bx - nx, by - ny), (bx + nx, by + ny)]
        ax.add_patch(Polygon(poly, closed=True, color=COL.get(traci.vehicle.getTypeID(v), "k"), zorder=4, lw=0))
    ax.set_title(title, fontsize=10)

def legend(ax):
    for k, c in COL.items():
        ax.plot([], [], "s", color=c, label=k)
    ax.legend(loc="upper right", fontsize=7, ncol=6, frameon=False)

traci.start(["sumo", "-c", os.path.join(SCN, "corridor.sumocfg"), "--seed", "42", "--no-warnings", "true"])
cx, cy = net.getNode("J2").getCoord()
frames, t = [], 0
while t < 900:
    traci.simulationStep(); t += 1
    if t in (420, 600):
        # overview
        PX = 0.9
        fig, ax = plt.subplots(figsize=(14, 4.2), dpi=150)
        draw_net(ax); draw_frame(ax, f"SUMO corridor4 — real simulation state at t={t}s ({traci.vehicle.getIDCount()} vehicles)")
        legend(ax); ax.set_aspect("equal"); ax.axis("off")
        b = net.getBBoxXY(); ax.set_xlim(b[0][0] - 10, b[1][0] + 10); ax.set_ylim(cy - 160, cy + 160)
        fig.savefig(os.path.join(OUT, f"overview_t{t}.png"), bbox_inches="tight"); plt.close(fig)
    if 360 <= t < 480:
        PX = 9.0
        fig, ax = plt.subplots(figsize=(8, 6), dpi=110)
        draw_net(ax); draw_frame(ax, f"Junction J2 close-up, t={t}s — two-wheelers filter laterally (sublane 0.4 m)")
        legend(ax); ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(cx - 90, cx + 30); ax.set_ylim(cy - 40, cy + 50)
        p = os.path.join(OUT, f"zoom_{t:04d}.png"); fig.savefig(p); plt.close(fig); frames.append(p)
traci.close()

try:
    from PIL import Image
    imgs = [Image.open(p).convert("P", palette=Image.ADAPTIVE) for p in frames[::2]]
    imgs[0].save(os.path.join(OUT, "j2_closeup.gif"), save_all=True, append_images=imgs[1:], duration=120, loop=0)
    print("gif ok")
except ImportError:
    print("no PIL; frames only")
print("done", len(frames))
