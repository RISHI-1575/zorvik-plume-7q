"""Figures for the Phase-I report (Times New Roman, 300 dpi)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent / "fig2"
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 11})
INK, BLUE, TEAL, SAND, GREY = "#1b2a3a", "#d6e6f5", "#d9efe6", "#f7ead0", "#eeeeee"


def box(ax, x, y, w, h, text, fc, fs=10, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=fc, ec=INK, lw=1.1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", wrap=True)


def arrow(ax, a, b, style="-|>", ls="-", color=INK, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=12, lw=1.1,
                                 color=color, ls=ls, connectionstyle=f"arc3,rad={rad}"))


# ---------- Fig 1.1 vehicle share vs PCU share (measured in our corridor) ----------
def share():
    t = ["Two-wheeler", "Auto-rickshaw", "Car", "Bus", "Truck"]
    veh = [44.7, 15.1, 22.0, 8.0, 10.2]   # measured: tripinfo_fixed_h8-9_s0.xml
    pcu = [19.1, 15.5, 18.8, 20.6, 26.0]   # same run, weighted by config.PCU
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    x = range(len(t)); w = 0.38
    b1 = ax.bar([i - w / 2 for i in x], veh, w, label="Share of vehicles (%)", color="#6b8fb3", ec=INK, lw=.6)
    b2 = ax.bar([i + w / 2 for i in x], pcu, w, label="Share of road load in PCU (%)", color="#e0a458", ec=INK, lw=.6)
    for b in list(b1) + list(b2):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + .6, f"{b.get_height():.1f}",
                ha="center", fontsize=8.5)
    ax.set_xticks(list(x), t); ax.set_ylabel("Percent"); ax.set_ylim(0, 52)
    ax.legend(frameon=False, fontsize=9); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT / "share.png", dpi=300); plt.close(fig)


# ---------- Fig 3.1 architecture ----------
def arch():
    fig, ax = plt.subplots(figsize=(7.2, 5.6)); ax.set_xlim(0, 12); ax.set_ylim(0, 9.4); ax.axis("off")
    # layer frames
    for y, h, lab, fc in [(6.55, 2.6, "A.  ENVIRONMENT  (SUMO, sublane model)", BLUE),
                          (2.85, 3.35, "B.  CONTROLLER  (one agent per junction)", TEAL),
                          (0.1, 2.4, "C.  EVALUATION", SAND)]:
        ax.add_patch(FancyBboxPatch((0.15, y), 11.7, h, boxstyle="round,pad=0.02,rounding_size=0.2",
                                    fc=fc, ec=INK, lw=1.3, alpha=.55))
        ax.text(0.4, y + h - 0.3, lab, fontsize=10.5, fontweight="bold", va="center")
    box(ax, 0.5, 6.8, 3.4, 1.6, "Mixed-traffic demand\nbike, auto, car, bus, truck\n(hourly profile)", "white", 9.5)
    box(ax, 4.3, 6.8, 3.4, 1.6, "4-junction corridor\nJ1 – J2 – J3 – J4\nlateral filtering on", "white", 9.5)
    box(ax, 8.1, 6.8, 3.4, 1.6, "Field check\nmanual counts at 2 junctions\n+ OpenCity timing sheets", "white", 9.5)
    arrow(ax, (3.9, 7.6), (4.3, 7.6)); arrow(ax, (8.1, 7.6), (7.7, 7.6))
    box(ax, 0.5, 4.35, 2.55, 1.3, "PCU-aware\nsensing", "white", 9.5, True)
    box(ax, 3.35, 4.35, 2.55, 1.3, "PPO policy\n(shared weights)", "white", 9.5, True)
    box(ax, 6.2, 4.35, 2.55, 1.3, "Safety shell\nmin/max green\nyellow, all-red", "white", 8.5, True)
    box(ax, 9.05, 4.35, 2.45, 1.3, "Signal\nphase command", "white", 9.5, True)
    for a, b in [((3.05, 5.0), (3.35, 5.0)), ((5.9, 5.0), (6.2, 5.0)), ((8.75, 5.0), (9.05, 5.0))]:
        arrow(ax, a, b)
    box(ax, 0.5, 3.05, 3.4, 0.95, "Neighbour messages\n(PCU released, ETA, priority)", "white", 9)
    box(ax, 4.3, 3.05, 3.4, 0.95, "Ambulance priority +\ncross-street recovery", "white", 9)
    box(ax, 8.1, 3.05, 3.4, 0.95, "Nightly retraining\non the day's logs", "white", 9)
    arrow(ax, (2.2, 4.0), (2.2, 4.35)); arrow(ax, (6.0, 4.0), (7.0, 4.35)); arrow(ax, (9.0, 4.0), (5.2, 4.35))
    arrow(ax, (6.0, 6.8), (1.8, 5.65), rad=.1)        # env -> sensing
    arrow(ax, (10.3, 5.65), (6.6, 6.8), rad=.1)       # command -> env
    box(ax, 0.5, 0.35, 3.4, 1.55, "Baselines\nFixed-time, Max Pressure,\nMPLight, CoLight", "white", 9.5)
    box(ax, 4.3, 0.35, 3.4, 1.55, "Same seeds,\nsame demand,\nsame corridor", "white", 9.5)
    box(ax, 8.1, 0.35, 3.4, 1.55, "Metrics\ndelay, ambulance time,\nrecovery time, per-class delay", "white", 9.5)
    arrow(ax, (3.9, 1.1), (4.3, 1.1)); arrow(ax, (7.7, 1.1), (8.1, 1.1))
    arrow(ax, (10.3, 3.05), (10.3, 1.9), ls="--")
    fig.tight_layout(); fig.savefig(OUT / "arch.png", dpi=300); plt.close(fig)


# ---------- Fig 3.2 sequence diagram ----------
def seq():
    lanes = ["SUMO\nsimulator", "Sensing\n(PCU)", "PPO agent\n(junction i)", "Neighbour\nj", "Safety\nshell", "Traffic\nsignal"]
    fig, ax = plt.subplots(figsize=(7.4, 6.4)); ax.set_xlim(0, 12); ax.set_ylim(0, 11); ax.axis("off")
    xs = [1 + i * 2 for i in range(len(lanes))]
    for x, l in zip(xs, lanes):
        box(ax, x - 0.85, 9.9, 1.7, 0.95, l, BLUE, 9, True)
        ax.plot([x, x], [0.4, 9.9], color="#8894a0", lw=1, ls=(0, (4, 3)))
    msgs = [(0, 1, "1. lane states (every 5 s)"),
            (1, 2, "2. PCU queue per approach"),
            (3, 2, "3. message: PCU released, ETA, flag"),
            (2, 2, "4. build observation"),
            (2, 4, "5. proposed phase"),
            (4, 4, "6. check min/max green"),
            (4, 5, "7. yellow + all-red, then green"),
            (5, 0, "8. apply phase via TraCI"),
            (2, 3, "9. send own message downstream"),
            (0, 2, "10. reward = −delay (training only)")]
    y = 9.3
    for a, b, t in msgs:
        if a == b:
            ax.add_patch(FancyArrowPatch((xs[a], y), (xs[a], y - 0.35), arrowstyle="-|>", mutation_scale=10,
                                         connectionstyle="arc3,rad=-1.6", lw=1, color=INK))
            ax.text(xs[a] + 0.35, y - 0.1, t, fontsize=8.8, va="center")
        else:
            arrow(ax, (xs[a], y), (xs[b], y))
            ax.text((xs[a] + xs[b]) / 2, y + 0.14, t, fontsize=8.8, ha="center", va="bottom")
        y -= 0.85
    ax.add_patch(FancyBboxPatch((0.2, 0.45), 11.6, 0.65, boxstyle="round,pad=0.02", fc=SAND, ec=INK, lw=.8))
    ax.text(6, 0.77, "Ambulance detected: priority flag set → shell grants green on its approach → "
            "after it clears, recovery phase serves cross streets", fontsize=8.6, ha="center", va="center")
    fig.tight_layout(); fig.savefig(OUT / "seq.png", dpi=300); plt.close(fig)


# ---------- Fig 3.3 corridor ----------
def corridor():
    fig, ax = plt.subplots(figsize=(7.0, 2.6)); ax.set_xlim(0, 12); ax.set_ylim(0, 4.2); ax.axis("off")
    ax.add_patch(plt.Rectangle((0.2, 1.7), 11.6, 0.8, fc=GREY, ec=INK, lw=.8))
    for i, x in enumerate([1.8, 4.6, 7.4, 10.2]):
        ax.add_patch(plt.Rectangle((x - 0.4, 0.2), 0.8, 3.8, fc=GREY, ec=INK, lw=.8))
        ax.add_patch(plt.Circle((x, 2.1), 0.33, fc=TEAL, ec=INK, lw=1))
        ax.text(x, 2.1, f"J{i+1}", ha="center", va="center", fontsize=9, fontweight="bold")
        if i < 3:
            arrow(ax, (x + 0.45, 3.2), (x + 2.35, 3.2), style="<|-|>", color="#2f6b9a")
            ax.text(x + 1.4, 3.42, "messages", ha="center", fontsize=8, color="#2f6b9a")
    ax.text(6.0, 1.3, "Main arterial  (sublane resolution 0.4 m)", fontsize=8.5, ha="center", bbox=dict(fc="white", ec="none", pad=1))
    ax.text(6.0, 0.35, "Side streets at every junction  ·  green wave along the arterial", fontsize=8.5, ha="center", bbox=dict(fc="white", ec="none", pad=1))
    fig.tight_layout(); fig.savefig(OUT / "corridor.png", dpi=300); plt.close(fig)


# ---------- Fig 3.4 preliminary baselines ----------
def baseline():
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    names = ["Fixed-time", "Max Pressure"]; d = [66.5, 46.4]; tt = [138.9, 118.9]
    x = [0, 1]; w = .36
    b1 = ax.bar([i - w / 2 for i in x], d, w, label="Mean delay (s)", color="#6b8fb3", ec=INK, lw=.6)
    b2 = ax.bar([i + w / 2 for i in x], tt, w, label="Mean travel time (s)", color="#e0a458", ec=INK, lw=.6)
    for b in list(b1) + list(b2):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 2, f"{b.get_height():.1f}", ha="center", fontsize=9)
    ax.set_xticks(x, names); ax.set_ylabel("Seconds"); ax.set_ylim(0, 160)
    ax.legend(frameon=False, fontsize=9); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT / "baseline.png", dpi=300); plt.close(fig)


# ---------- Fig 3.2 flowchart of the proposed algorithm ----------
def flow():
    fig, ax = plt.subplots(figsize=(6.0, 8.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 25.5); ax.axis("off")
    steps = [
        ("SUMO advances one simulation step\n(TraCI reads every vehicle)", BLUE),
        ("PCU-weighted queue per approach\nQ$_a$(t) from halted vehicles", BLUE),
        ("Add neighbour messages\n(PCU released, ETA, priority flag)", TEAL),
        ("Build observation s$_t$\n(queues, phase, green time, hour)", TEAL),
        ("PPO policy samples an action\nkeep phase / switch phase", SAND),
    ]
    y = 23.0
    prev = None
    for txt, fc in steps:
        box(ax, 1.6, y, 6.8, 1.7, txt, fc, fs=9)
        if prev is not None:
            arrow(ax, (5.0, prev), (5.0, y + 1.7))
        prev = y; y -= 2.6
    # ambulance decision diamond
    dy = y + 0.85
    dia = plt.Polygon([(5.0, dy + 1.25), (8.2, dy), (5.0, dy - 1.25), (1.8, dy)],
                      fc="#f6dede", ec=INK, lw=1.1)
    ax.add_patch(dia)
    ax.text(5.0, dy, "Ambulance on\nthis approach?", ha="center", va="center", fontsize=9)
    arrow(ax, (5.0, prev), (5.0, dy + 1.25))
    box(ax, 0.2, dy - 1.0, 1.5, 2.0, "yes:\nforce\nambulance\nphase", "#f6dede", fs=8)
    arrow(ax, (1.8, dy), (1.7, dy))
    ax.text(5.2, dy - 1.62, "no", fontsize=8.5)
    # safety shell
    y = dy - 4.0
    box(ax, 1.6, y, 6.8, 2.1,
        "Safety shell\nmin green 10 s  ·  max green 60 s\nyellow 3 s  ·  all-red 2 s", "#e9e2f6", fs=9)
    arrow(ax, (5.0, dy - 1.25), (5.0, y + 2.1))
    arrow(ax, (0.95, dy - 1.0), (0.95, y + 1.05)); arrow(ax, (0.95, y + 1.05), (1.6, y + 1.05))
    y2 = y - 2.6
    box(ax, 1.6, y2, 6.8, 1.7, "Approved phase written to the signal\nthrough TraCI", SAND, fs=9)
    arrow(ax, (5.0, y), (5.0, y2 + 1.7))
    y3 = y2 - 2.6
    box(ax, 1.6, y3, 6.8, 1.7,
        "Send message to neighbours,\ncompute reward r$_t$, store transition", BLUE, fs=9)
    arrow(ax, (5.0, y2), (5.0, y3 + 1.7))
    # loop back
    arrow(ax, (8.4, y3 + 0.85), (9.4, y3 + 0.85))
    arrow(ax, (9.4, y3 + 0.85), (9.4, 23.85)); arrow(ax, (9.4, 23.85), (8.4, 23.85))
    ax.text(9.6, 12.0, "next decision step (5 s)", rotation=90, va="center", fontsize=8.5)
    fig.tight_layout(); fig.savefig(OUT / "flow.png", dpi=300); plt.close(fig)


for f in (share, arch, seq, corridor, baseline, flow):
    f()
print("ok", sorted(p.name for p in OUT.iterdir()))
