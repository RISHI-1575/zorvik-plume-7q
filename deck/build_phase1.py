#!/usr/bin/env python
"""Saarathi — Phase I Literature Survey Review deck (BNMIT official template)."""
import io, zipfile
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import sys; sys.path.insert(0, str(Path(__file__).resolve().parent))
from papers import LIT, REFS

TPL = Path("/Users/rishi/Downloads/9.2 Phase I Literature Survey Review PPT Template - Copy.pptx")
OUT = Path(__file__).resolve().parent / "Saarathi_Phase1_LiteratureSurvey.pptx"
TNR = "Times New Roman"
BLACK = RGBColor(0, 0, 0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HDR = RGBColor(0xD9, 0xD9, 0xD9)
LITE = RGBColor(0xF2, 0xF2, 0xF2)
DARK = RGBColor(0x3A, 0x3A, 0x3A)

LOGO = zipfile.ZipFile(str(TPL)).read('ppt/media/image1.jpeg')
prs = Presentation(str(TPL))
LAYOUT = prs.slide_master.slide_layouts.get_by_name("Title and Content")


# ------------------------------------------------------------------ helpers
def move_slide(slide, pos):
    lst = prs.slides._sldIdLst
    el = next(e for e in list(lst) if int(e.get('id')) == slide.slide_id)
    lst.remove(el); lst.insert(pos, el)


def new_slide(at=None):
    s = prs.slides.add_slide(LAYOUT)
    s.shapes.add_picture(io.BytesIO(LOGO), Inches(0.17), Inches(0.19),
                         Inches(1.46), Inches(1.43))
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx == 11:
            ph.text_frame.text = "Dept of AIML, BNMIT"
            for p in ph.text_frame.paragraphs:
                for r in p.runs:
                    r.font.name = TNR; r.font.size = Pt(12); r.font.color.rgb = BLACK
    if at is not None:
        move_slide(s, at)
    return s


def by_ph(slide, idx):
    for sh in slide.shapes:
        if sh.is_placeholder and sh.placeholder_format.idx == idx:
            return sh


def set_title(slide, text, size=32):
    ph = by_ph(slide, 0)
    ph.left, ph.top, ph.width, ph.height = (Inches(1.72), Inches(0.30),
                                            Inches(7.85), Inches(1.15))
    tf = ph.text_frame
    tf.clear(); tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.name = TNR; r.font.size = Pt(size); r.font.bold = True
    r.font.color.rgb = BLACK


def body(slide, items, box=None):
    """items: (text, size, bold, level)."""
    sh = by_ph(slide, 1)
    if sh is None:
        sh = slide.shapes.add_textbox(Inches(0.5), Inches(1.75), Inches(9.0), Inches(4.95))
    if box:
        sh.left, sh.top, sh.width, sh.height = [Inches(v) for v in box]
    tf = sh.text_frame
    tf.clear(); tf.word_wrap = True
    for i, (text, size, bold, lvl) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = lvl
        r = p.add_run(); r.text = text
        r.font.name = TNR; r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = BLACK
        p.space_after = Pt(5)
    return sh


def cell(c, text, size=10, bold=False, align=PP_ALIGN.LEFT, fill=None):
    c.text = ""
    c.vertical_anchor = MSO_ANCHOR.MIDDLE
    c.margin_left = c.margin_right = Inches(0.04)
    c.margin_top = c.margin_bottom = Inches(0.015)
    if fill is not None:
        c.fill.solid(); c.fill.fore_color.rgb = fill
    p = c.text_frame.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.name = TNR; r.font.size = Pt(size); r.font.bold = bold
    r.font.color.rgb = BLACK


def table(slide, rows, cols, l, t, w, h, widths=None):
    sh = slide.shapes.add_table(rows, cols, Inches(l), Inches(t), Inches(w), Inches(h))
    tbl = sh.table
    if widths:
        for i, ww in enumerate(widths):
            tbl.columns[i].width = Inches(ww)
    return tbl


def box(slide, l, t, w, h, text, sub=None, size=10.5, fill=WHITE,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, bold=True):
    s = slide.shapes.add_shape(shape, Inches(l), Inches(t), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    s.line.color.rgb = DARK; s.line.width = Pt(1)
    s.shadow.inherit = False
    tf = s.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.03)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.name = TNR; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = BLACK
    if sub:
        p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run(); r2.text = sub
        r2.font.name = TNR; r2.font.size = Pt(size - 1.5); r2.font.color.rgb = BLACK
    return s


def arrow(slide, x1, y1, x2, y2):
    from pptx.oxml.ns import qn
    c = slide.shapes.add_connector(2, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = DARK; c.line.width = Pt(1.25)
    ln = c.line._get_or_add_ln()
    ln.append(ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'h': 'med'}))
    return c


def label(slide, l, t, w, h, text, size=9.5, bold=False, align=PP_ALIGN.LEFT, italic=False):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.name = TNR; r.font.size = Pt(size); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = BLACK
    return tb


# ================================================================== CONTENT

TEAM = [("P Yukthesh", "1BG23AI068"),
        ("Rishi Shashikanth", "1BG23AI083"),
        ("Vimal", "1BG24AI411")]

# ---- 0 Title ----
s0 = prs.slides[0]
tf = by_ph(s0, 0).text_frame
tf.clear()
for i, (t, sz, bd) in enumerate([
        ("Project Work Phase I (Literature Survey Review)", 26, False),
        ("", 12, False),
        ("Saarathi: A Self-Learning Decentralised Traffic Signal Control "
         "System with Coordinated Green Waves and Emergency Priority Corridors", 28, True)]):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t
    r.font.name = TNR; r.font.size = Pt(sz); r.font.bold = bd; r.font.color.rgb = BLACK

tf = by_ph(s0, 1).text_frame
tf.clear()
rows = [("Presented by", 16, True),
        ("", 10, False),
        ("   ".join(n for n, _ in TEAM), 15, True),
        ("        ".join(u for _, u in TEAM), 14, False),
        ("", 10, False),
        ("Under the guidance of", 15, True),
        ("<Guide Name>", 15, False),
        ("<Designation>", 14, False),
        ("Department of Artificial Intelligence & Machine Learning", 14, False),
        ("BNM Institute of Technology, Bengaluru - 560070", 14, False)]
for i, (t, sz, bd) in enumerate(rows):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t
    r.font.name = TNR; r.font.size = Pt(sz); r.font.bold = bd; r.font.color.rgb = BLACK

# ---- 1 Organization ----
s = prs.slides[1]
set_title(s, "Organization of the Presentation", 32)
body(s, [(t, 20, False, 0) for t in
         ["Introduction", "Aim & Scope of the Work", "Problem Statement",
          "Objectives", "Literature Survey", "Research Gap",
          "Proposed System Design", "Methodology", "Project Plan", "References"]],
     box=(1.72, 1.70, 7.85, 5.05))

# ---- 2 Introduction ----
s = prs.slides[2]
set_title(s, "Introduction", 32)
body(s, [
 ("Traffic signals decide how road capacity is shared at an intersection. Their control logic "
  "therefore sets the delay, the number of stops and the idling emissions of every vehicle that "
  "passes through.", 15, False, 0),
 ("Three control families are in field use today:", 15, True, 0),
 ("Fixed-time control: pre-computed plans from historical counts; cannot respond to the "
  "actual demand present at the junction.", 14, False, 1),
 ("Vehicle-actuated control: extends a green while detectors stay occupied; reacts only to "
  "one approach, with no view of the network.", 14, False, 1),
 ("Adaptive control (SCATS, SCOOT, CoSiCoSt/BATCS): re-optimises cycle, split and offset "
  "using hand-designed rules and calibrated parameters.", 14, False, 1),
 ("Adaptive systems are rule-based. Their parameters are tuned by engineers at commissioning "
  "and are not revised automatically as demand patterns change.", 15, False, 0),
 ("Reinforcement learning (RL) offers control policies learned directly from observed traffic "
  "state, and has been studied for signal control for over a decade "
  "(Wei et al. 2019; Chu et al. 2020; Noaeen et al. 2022).", 15, False, 0),
], box=(0.5, 1.60, 9.0, 5.15))

# ---- Introduction (Indian / Bengaluru context) : new slide at 3 ----
s = new_slide()
INTRO2 = s
set_title(s, "Introduction – Indian Traffic Context", 30)
body(s, [
 ("Indian urban traffic is heterogeneous and lane-less: two-wheelers, autorickshaws, cars, "
  "buses and trucks share the same carriageway and do not maintain lane discipline.", 15, False, 0),
 ("Vehicle counts alone are therefore a poor measure of demand; Indian practice converts the "
  "mixed stream into Passenger Car Units (PCU) as specified in IRC 106-1990.", 15, False, 0),
 ("Bengaluru operates BATCS (Bengaluru Adaptive Traffic Control System), based on C-DAC's "
  "indigenous CoSiCoSt adaptive controller designed for heterogeneous traffic.", 15, False, 0),
 ("155 existing junctions were upgraded and 14 new ones added, giving 169 adaptive "
  "signalised junctions under full-scale operation from April 2025.", 14, False, 1),
 ("The deployment reports a 33% reduction in travel time on the Hudson Circle corridor and "
  "is designed to scale to 500+ junctions.", 14, False, 1),
 ("Consequence: camera-based detection and networked adaptive controllers are already "
  "installed in the city. A learning control layer is therefore a software addition to "
  "existing infrastructure, not a new hardware deployment.", 15, False, 0),
], box=(0.5, 1.60, 9.0, 5.15))

# ---- 4 Aim & Scope ----
s = prs.slides[3]
set_title(s, "Aim & Scope of the Project", 32)
body(s, [
 ("Aim", 20, True, 0),
 ("To develop a decentralised, self-learning traffic signal control system in which every "
  "junction learns its own time-varying demand pattern, coordinates with adjacent junctions "
  "to form green waves along a corridor, and grants priority corridors to emergency and "
  "escorted vehicles, operating as a software layer over existing adaptive-signal "
  "infrastructure.", 15, False, 1),
 ("Scope", 20, True, 0),
 ("A corridor of four signalised junctions modelled in SUMO with the sub-lane model enabled "
  "to represent lane-less movement.", 14, False, 1),
 ("Demand measured in PCU from a mixed vehicle stream; no per-class vehicle "
  "classification is assumed.", 14, False, 1),
 ("One learning agent per junction; neighbour coordination through a compact message, "
  "not through a central optimiser.", 14, False, 1),
 ("A non-learned safety layer enforcing minimum green, maximum green, yellow and all-red "
  "intervals at all times.", 14, False, 1),
 ("Evaluation in simulation against fixed-time, vehicle-actuated, max-pressure and a "
  "rule-based adaptive baseline.", 14, False, 1),
 ("Out of scope: field deployment on live signals, connected-vehicle infrastructure, and "
  "pedestrian-demand modelling.", 14, False, 1),
], box=(0.5, 1.60, 9.0, 5.15))

# ---- 5 Problem Statement ----
s = prs.slides[4]
set_title(s, "Problem Statement", 32)
body(s, [
 ("Deployed adaptive signal controllers optimise using fixed, hand-tuned rules. They do not "
  "learn from the traffic they observe, and their parameters are not automatically revised "
  "when demand patterns shift.", 16, False, 0),
 ("Reported RL controllers are trained and tested on the same demand distribution. Robustness "
  "to time-of-day variation, weekday-weekend variation and demand shift is rarely evaluated, "
  "so field behaviour under changing conditions remains unestablished.", 16, False, 0),
 ("Coordination and emergency-vehicle priority are studied as separate problems, requiring "
  "separate subsystems at deployment.", 16, False, 0),
 ("Emergency priority is commonly implemented as full pre-emption, which clears the priority "
  "path but transfers the delay to the cross streets with no defined recovery.", 16, False, 0),
 ("Problem: to design a signal control system that learns each junction's own demand pattern, "
  "sustains that performance as the pattern changes, and delivers coordination and priority "
  "through a single mechanism, under enforced safety constraints.", 16, True, 0),
], box=(0.5, 1.60, 9.0, 5.15))

# ---- 6 Objectives ----
s = prs.slides[5]
set_title(s, "Objectives", 32)
body(s, [
 ("To model a four-junction Bengaluru corridor in SUMO using the sub-lane model, with "
  "heterogeneous PCU-weighted demand and a 24-hour time-of-day profile.", 15, False, 0),
 ("To design a per-junction reinforcement learning agent whose state includes approach-wise "
  "PCU occupancy together with an explicit time-of-day and day-of-week encoding.", 15, False, 0),
 ("To implement a non-learned safety shell that enforces minimum green, maximum green, yellow "
  "and all-red intervals on every action issued by the agent.", 15, False, 0),
 ("To implement neighbour-to-neighbour platoon messaging carrying released PCU, estimated "
  "arrival time and a priority flag, so that green waves form without a central controller.", 15, False, 0),
 ("To realise emergency and escorted-vehicle priority on the same messaging channel as a "
  "priority corridor with a defined cross-street recovery policy, in place of full pre-emption.", 15, False, 0),
 ("To establish a continual learning loop in which the agent is periodically retrained and "
  "validated on a simulation twin before any updated policy is accepted.", 15, False, 0),
 ("To evaluate the system against fixed-time, vehicle-actuated, max-pressure and rule-based "
  "adaptive baselines on delay, stops, throughput and priority-vehicle travel time, including "
  "unseen demand conditions.", 15, False, 0),
], box=(0.5, 1.55, 9.0, 5.25))

# ---- 7 & 8 Literature Survey ----
HEAD = ["Sl. No.", "Paper Title, Author, Publication details", "Methodology Used", "Drawbacks"]
WID = [0.55, 3.45, 2.60, 2.40]


def lit_table(slide, start, end):
    n = end - start
    tbl = table(slide, n + 1, 4, 0.48, 1.52, 9.02, 0.28 * (n + 1), WID)
    for j, h in enumerate(HEAD):
        cell(tbl.cell(0, j), h, size=11, bold=True, align=PP_ALIGN.CENTER, fill=HDR)
    for i in range(n):
        t, m, d = LIT[start + i]
        cell(tbl.cell(i + 1, 0), str(start + i + 1), size=9, align=PP_ALIGN.CENTER,
             fill=LITE if i % 2 else WHITE)
        for j, txt in enumerate((t, m, d), start=1):
            cell(tbl.cell(i + 1, j), txt, size=9, fill=LITE if i % 2 else WHITE)
    return tbl


s = prs.slides[6]
set_title(s, "Literature Survey", 32)
sh = by_ph(s, 1)
sh._element.getparent().remove(sh._element)
lit_table(s, 0, 10)

s = prs.slides[7]
set_title(s, "Literature Survey (contd.)", 30)
sh = by_ph(s, 1)
sh._element.getparent().remove(sh._element)
lit_table(s, 10, 20)

# ---- Research Gap : new slide ----
s = new_slide()
GAP = s
set_title(s, "Research Gap", 32)
body(s, [
 ("Generalisation is not evaluated. Reported RL controllers are trained and tested on the "
  "same demand distribution; surveys from 2025 identify robustness across time-of-day, "
  "weekday-weekend and demand shift as unresolved (papers 4, 6).", 15, False, 0),
 ("Non-stationarity is not handled operationally. Continual learning methods exist in the "
  "general literature but are not instantiated as a retrain-validate-deploy procedure for "
  "signal control (paper 10).", 15, False, 0),
 ("Safety is penalised, not enforced. Constraint-aware formulations use soft penalties, so "
  "minimum-green and clearance intervals can still be violated during exploration (paper 9).", 15, False, 0),
 ("Coordination and priority are separate subsystems. Cooperative control (papers 14, 19, 20) "
  "and emergency priority (papers 12, 15) are developed independently, requiring two "
  "mechanisms in deployment.", 15, False, 0),
 ("Pre-emption has no defined recovery. Existing work quantifies cross-street delay caused by "
  "pre-emption but does not specify how the cross streets are restored afterwards (paper 12).", 15, False, 0),
 ("Indian heterogeneous traffic is under-represented. Standard benchmarks are lane-based; "
  "PCU-based lane-less studies control junctions in isolation (papers 11, 13, 17).", 15, False, 0),
], box=(0.5, 1.60, 9.0, 5.15))

# ---- 10 Proposed System Design – Architecture ----
s = prs.slides[8]
set_title(s, "Proposed System Design – System Architecture", 26)
sh = by_ph(s, 1); sh._element.getparent().remove(sh._element)

box(s, 0.55, 1.72, 4.20, 0.46, "Camera / Loop Detectors at Junction k", size=11)
box(s, 5.25, 1.72, 4.20, 0.46, "Priority Beacon — ambulance / escorted convoy", size=11)
box(s, 0.55, 2.46, 8.90, 0.46,
    "PCU Estimator — approach-wise demand in Passenger Car Units (IRC 106-1990)", size=11)
box(s, 0.55, 3.20, 8.90, 0.78, "Junction Agent k — learned policy (PPO)",
    sub="state: approach PCU · current phase · time in phase · time-of-day (sin/cos) · "
        "weekday flag · neighbour message", size=11.5)
box(s, 0.55, 4.26, 8.90, 0.46,
    "Safety Shell (non-learned) — min green 10 s · max green 60 s · yellow 3 s · all-red 2 s",
    size=11)
box(s, 0.55, 5.00, 4.20, 0.46, "Signal Controller at Junction k", size=11)
box(s, 5.25, 5.00, 4.20, 0.46, "Neighbour Message Bus", size=11)
box(s, 0.55, 5.74, 4.20, 0.52, "Nightly Simulation Twin",
    sub="retrain → validate → deploy gate", size=10.5)
box(s, 5.25, 5.74, 4.20, 0.52, "Adjacent Junction Agents k-1, k+1",
    sub="(PCU released, ETA, priority flag)", size=10.5)

for a in [(2.65, 2.18, 2.65, 2.46), (7.35, 2.18, 7.35, 2.46),
          (5.00, 2.92, 5.00, 3.20), (5.00, 3.98, 5.00, 4.26),
          (2.65, 4.72, 2.65, 5.00), (7.35, 4.72, 7.35, 5.00),
          (2.65, 5.46, 2.65, 5.74), (7.35, 5.46, 7.35, 5.74)]:
    arrow(s, *a)
arrow(s, 7.35, 4.49, 7.35, 5.00)
label(s, 0.55, 6.32, 8.90, 0.30,
      "Every junction runs the same stack independently; coordination and priority travel on "
      "one message channel.", size=10, align=PP_ALIGN.CENTER, italic=True)

# ---- 11 Proposed System Design – Sequence ----
s = prs.slides[9]
set_title(s, "Proposed System Design – Sequence Diagram", 26)
sh = by_ph(s, 1); sh._element.getparent().remove(sh._element)

LIFE = ["Detector /\nPCU Estimator", "Junction\nAgent k", "Safety\nShell",
        "Signal\nController k", "Neighbour\nAgent k+1"]
CX = [1.05, 3.05, 5.00, 6.95, 8.90]
for name, cx in zip(LIFE, CX):
    b = box(s, cx - 0.82, 1.68, 1.64, 0.50, name.replace("\n", " "), size=9.5)
    ln = s.shapes.add_connector(1, Inches(cx), Inches(2.18), Inches(cx), Inches(6.45))
    ln.line.color.rgb = DARK; ln.line.width = Pt(0.75)

MSG = [(0, 1, "approach PCU + time-of-day context"),
       (1, 2, "proposed action (hold / switch phase)"),
       (2, 3, "validated phase command"),
       (3, 1, "realised phase, time in phase"),
       (1, 4, "platoon message (PCU released, ETA, priority 0)"),
       (0, 1, "priority vehicle detected (priority 1 / 2)"),
       (1, 4, "priority corridor request (ETA, priority level)"),
       (4, 1, "corridor acknowledged, offset applied"),
       (1, 2, "extend green on priority approach"),
       (2, 3, "command issued within safety limits"),
       (1, 4, "priority cleared → cross-street recovery")]
y = 2.60
for a, b_, txt in MSG:
    x1, x2 = CX[a], CX[b_]
    arrow(s, x1, y, x2, y)
    mid = (x1 + x2) / 2
    label(s, mid - 1.85, y - 0.30, 3.70, 0.28, txt, size=8.5, align=PP_ALIGN.CENTER)
    y += 0.36

# ---- 12 Methodology ----
s = prs.slides[10]
set_title(s, "Methodology – Proposed Model", 30)
body(s, [
 ("Algorithm / Proposed model", 15, True, 0),
 ("Corridor model: four-junction SUMO network with the sub-lane model enabled; mixed "
  "vehicle stream converted to PCU; 24-hour demand profile with weekday and weekend variants.",
  11.5, False, 1),
 ("Control formulation: one Markov decision process per junction. State = approach PCU, "
  "current phase, time in phase, time-of-day (sin/cos) and weekday flag. Action = hold or "
  "advance to the next phase, evaluated every 5 s. Reward = negative PCU-weighted delay with "
  "a switching penalty.", 11.5, False, 1),
 ("Policy learning: Proximal Policy Optimisation (PPO), warm-started by behaviour cloning of "
  "a fixed-time plan so that early policies are usable.", 11.5, False, 1),
 ("Safety shell: a non-learned wrapper that clamps every action to minimum green, maximum "
  "green, yellow and all-red constraints before it reaches the controller.", 11.5, False, 1),
 ("Coordination: on each phase termination the agent publishes (PCU released, estimated "
  "arrival time, priority flag) to its neighbours, which bias their own phase timing to "
  "receive the platoon.", 11.5, False, 1),
 ("Priority corridor: priority flag 1 (ambulance) and 2 (escorted convoy) raise the message "
  "precedence along the route; the safety shell remains in force and a recovery policy "
  "restores cross-street service after the vehicle passes.", 11.5, False, 1),
 ("Continual learning: the policy is periodically retrained on recent logged demand in a "
  "simulation twin and is deployed only if it validates above the incumbent.", 11.5, False, 1),
 ("Evaluation: delay, stops, throughput and priority-vehicle travel time against fixed-time, "
  "vehicle-actuated, max-pressure and rule-based adaptive baselines, on trained and on "
  "unseen demand.", 11.5, False, 1),
], box=(0.5, 1.50, 9.0, 5.40))

# ---- Methodology (rationale) : new slide ----
s = new_slide()
METH2 = s
set_title(s, "Methodology – Rationale and Evaluation", 28)
body(s, [
 ("Reason for choosing the proposed model", 15, True, 0),
 ("PPO is stable on small discrete action spaces and does not require the replay tuning that "
  "value-based methods need for non-stationary demand.", 11.5, False, 1),
 ("A per-junction agent avoids the joint action-space growth of centralised multi-agent "
  "control and allows one junction to be retrained without retraining the corridor.", 11.5, False, 1),
 ("A PCU state matches what camera-based detection at Indian junctions can actually supply; "
  "per-class vehicle classification is not required.", 11.5, False, 1),
 ("Enforcing safety outside the learned policy keeps the guarantee independent of training "
  "outcome, unlike soft-penalty formulations.", 11.5, False, 1),
 ("Evaluation plan", 15, True, 0),
 ("Metrics: average delay per vehicle, number of stops, corridor throughput and "
  "priority-vehicle travel time.", 11.5, False, 1),
 ("Baselines: fixed-time, vehicle-actuated, max-pressure and a rule-based adaptive "
  "controller of the CoSiCoSt type.", 11.5, False, 1),
 ("Conditions: demand seen during training, and unseen conditions formed by shifting the "
  "time-of-day profile and the total demand level.", 11.5, False, 1),
], box=(0.5, 1.55, 9.0, 5.30))

# ---- 13 Project Plan ----
s = new_slide()
GANTT = s
set_title(s, "Project Plan", 32)
MONTHS = ["Oct 2026", "Nov 2026", "Dec 2026", "Jan 2027", "Feb 2027", "Mar 2027"]
TASKS = [("Literature survey and problem formulation", 0, 1),
         ("Corridor model and PCU demand generation in SUMO", 0, 2),
         ("Baseline controllers: fixed-time, actuated, max-pressure", 1, 2),
         ("Safety shell and single-junction RL agent", 2, 3),
         ("Neighbour messaging and corridor green waves", 3, 4),
         ("Priority corridor and cross-street recovery", 4, 4),
         ("Continual retrain-validate-deploy loop", 4, 5),
         ("Evaluation, ablations and report writing", 5, 5)]
tbl = table(s, len(TASKS) + 1, 7, 0.48, 1.78, 9.02, 0.34 * (len(TASKS) + 1),
            [3.62] + [0.90] * 6)
cell(tbl.cell(0, 0), "Task", size=11, bold=True, align=PP_ALIGN.CENTER, fill=HDR)
for j, m in enumerate(MONTHS):
    cell(tbl.cell(0, j + 1), m, size=10, bold=True, align=PP_ALIGN.CENTER, fill=HDR)
for i, (t, a, b_) in enumerate(TASKS):
    cell(tbl.cell(i + 1, 0), t, size=10)
    for j in range(6):
        on = a <= j <= b_
        cell(tbl.cell(i + 1, j + 1), "", size=10,
             fill=RGBColor(0x59, 0x59, 0x59) if on else WHITE)

# ---- 14 References ----
s = prs.slides[11]
set_title(s, "References", 32)
body(s, [(f"[{i+1}] {r}", 8.5, False, 0) for i, r in enumerate(REFS)],
     box=(0.5, 1.62, 9.0, 5.28))

# ---- ordering ----
move_slide(INTRO2, 3)
move_slide(GAP, 9)
move_slide(METH2, 13)
move_slide(GANTT, 14)

prs.save(str(OUT))
print("saved", OUT, len(prs.slides.__iter__.__self__._sldIdLst))
