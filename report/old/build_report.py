#!/usr/bin/env python
"""Saarathi — Project Work Phase I Report (23AML175), BNMIT prescribed format."""
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = Path(__file__).resolve().parent
IMG = Path("/private/tmp/claude-501/-Users-rishi-Personal-final-year-project/"
           "6d2fbaa2-d8e9-42ff-ab6b-f87f005a987c/scratchpad")
OUT = HERE / "Saarathi_Phase1_Report.docx"

TITLE = ("Saarathi: A Self-Learning Decentralised Traffic Signal Control System "
         "with Coordinated Green Waves and Emergency Priority Corridors")
SHORT = "Saarathi: Self-Learning Decentralised Traffic Signal Control"
TEAM = [("P Yukthesh", "1BG23AI068"),
        ("Rishi Shashikanth", "1BG23AI083"),
        ("Vimal", "1BG24AI411")]
YEAR = "2026 – 2027"

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
st.paragraph_format.space_after = Pt(0)
st.paragraph_format.line_spacing = 1.5


TEXTW = 5.77  # A4 width 8.27in - 1.5in left - 1.0in right


def margins(sec):
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.left_margin = Inches(1.5)
    sec.right_margin = sec.top_margin = sec.bottom_margin = Inches(1.0)


def para(text="", size=12, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
         before=0, after=6, italic=False, spacing=1.5, caps=False):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    pf.line_spacing = spacing
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"; r.font.size = Pt(size)
        r.bold = bold; r.italic = italic
        r.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        if caps:
            r.font.all_caps = True
    return p


def set_pgnum(sec, start=None, fmt=None):
    """Set or clear the inherited w:pgNumType on a section."""
    sp = sec._sectPr
    pg = sp.find(qn("w:pgNumType"))
    if start is None and fmt is None:
        if pg is not None:
            sp.remove(pg)
        return
    if pg is None:
        pg = OxmlElement("w:pgNumType"); sp.append(pg)
    if start is not None:
        pg.set(qn("w:start"), str(start))
    if fmt is not None:
        pg.set(qn("w:fmt"), fmt)


def chapter_cover(num, name):
    """Own section, no header/footer, title 28pt centred."""
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    margins(sec)
    for h in (sec.header, sec.footer, sec.first_page_header, sec.first_page_footer):
        h.is_linked_to_previous = False
        for p in h.paragraphs:
            p.clear()
    set_pgnum(sec)
    for _ in range(9):
        para(after=0)
    para(f"CHAPTER {num}", 28, True, WD_ALIGN_PARAGRAPH.CENTER, after=24)
    para(name, 28, True, WD_ALIGN_PARAGRAPH.CENTER)
    return sec


def field(par, code):
    r = par.add_run()
    fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = code
    fc2 = OxmlElement("w:fldChar"); fc2.set(qn("w:fldCharType"), "end")
    r._r.append(fc); r._r.append(it); r._r.append(fc2)
    r.font.name = "Times New Roman"; r.font.size = Pt(12)


def chapter_body(restart=None):
    """Own section with header + footer."""
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    margins(sec)
    for h in (sec.header, sec.footer):
        h.is_linked_to_previous = False
    hp = sec.header.paragraphs[0]
    hp.text = ""
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = hp.add_run(SHORT)
    r.font.name = "Times New Roman"; r.font.size = Pt(10); r.italic = True

    sec.footer.paragraphs[0].text = ""
    ft = sec.footer.add_table(rows=1, cols=3, width=Inches(TEXTW))
    ft.autofit = False
    for cell, w, al in zip(ft.rows[0].cells, (2.3, 1.2, 2.27),
                           (WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER,
                            WD_ALIGN_PARAGRAPH.RIGHT)):
        cell.width = Inches(w)
        fp = cell.paragraphs[0]
        fp.alignment = al
        fp.paragraph_format.space_after = Pt(0)
        if al is WD_ALIGN_PARAGRAPH.CENTER:
            field(fp, " PAGE ")
            fp.runs[0].font.size = Pt(10)
        else:
            r = fp.add_run("B.E / Dept. of AIML / BNMIT" if al is WD_ALIGN_PARAGRAPH.LEFT
                           else YEAR.replace(" \u2013 ", "-"))
            r.font.name = "Times New Roman"; r.font.size = Pt(10)
    sec.footer.paragraphs[-1]._p.getparent().remove(sec.footer.paragraphs[-1]._p) \
        if len(sec.footer.paragraphs) > 1 else None

    set_pgnum(sec, restart)
    return sec


def heading(text, level):
    size = {1: 18, 2: 16, 3: 14}[level]
    return para(text, size, True, WD_ALIGN_PARAGRAPH.LEFT,
                before=12 if level > 1 else 0, after=10, spacing=1.15)


def figure(path, caption, width=TEXTW - 0.3):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(4)
    p.add_run().add_picture(str(path), width=Inches(width))
    para(caption, 11, True, WD_ALIGN_PARAGRAPH.CENTER, after=12, spacing=1.0)


def simple_table(rows, widths, header_bold=True, size=10):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.autofit = False
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(lay)
    k = TEXTW / sum(widths)
    widths = [w * k for w in widths]
    for j, w in enumerate(widths):          # tblGrid, not just the cells
        t.columns[j].width = Inches(w)
    for i, row in enumerate(rows):
        for j, txt in enumerate(row):
            c = t.cell(i, j)
            c.width = Inches(widths[j])
            c.text = ""
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            p.alignment = (WD_ALIGN_PARAGRAPH.CENTER if j == 0 or i == 0
                           else WD_ALIGN_PARAGRAPH.LEFT)
            r = p.add_run(txt)
            r.font.name = "Times New Roman"; r.font.size = Pt(size)
            r.bold = header_bold and i == 0
    return t


# ===================================================== FRONT MATTER (section 1)
s1 = doc.sections[0]
margins(s1)

para("VISVESVARAYA TECHNOLOGICAL UNIVERSITY", 16, True, WD_ALIGN_PARAGRAPH.CENTER,
     after=2, spacing=1.0)
para("JNANASANGAMA, BELAGAVI – 590018", 12, True, WD_ALIGN_PARAGRAPH.CENTER,
     after=18, spacing=1.0)
para("Project Work Phase I Report (23AML175)", 14, True, WD_ALIGN_PARAGRAPH.CENTER,
     after=4, spacing=1.0)
para("On", 12, False, WD_ALIGN_PARAGRAPH.CENTER, after=8, spacing=1.0)
para(TITLE.upper(), 15, True, WD_ALIGN_PARAGRAPH.CENTER, after=18, spacing=1.15)
para("Submitted by", 12, True, WD_ALIGN_PARAGRAPH.CENTER, after=6, spacing=1.0)
for n, u in TEAM:
    para(f"{n}\t{u}", 12, True, WD_ALIGN_PARAGRAPH.CENTER, after=2, spacing=1.0)
para("", 12, after=10, spacing=1.0)
para("Under the guidance of", 12, True, WD_ALIGN_PARAGRAPH.CENTER, after=4, spacing=1.0)
para("<Guide Name>", 12, True, WD_ALIGN_PARAGRAPH.CENTER, after=2, spacing=1.0)
para("<Designation>, Dept. of AIML, BNMIT, Bengaluru", 12, False,
     WD_ALIGN_PARAGRAPH.CENTER, after=18, spacing=1.0)
para("B.N.M. Institute of Technology", 14, True, WD_ALIGN_PARAGRAPH.CENTER,
     after=2, spacing=1.0)
para("An Autonomous Institution under VTU", 12, False, WD_ALIGN_PARAGRAPH.CENTER,
     after=2, spacing=1.0)
para("Approved by AICTE, Accredited as grade A Institution by NAAC", 11, False,
     WD_ALIGN_PARAGRAPH.CENTER, after=6, spacing=1.0)
para("Department of Artificial Intelligence and Machine Learning", 12, True,
     WD_ALIGN_PARAGRAPH.CENTER, after=6, spacing=1.0)
para(YEAR, 12, True, WD_ALIGN_PARAGRAPH.CENTER, spacing=1.0)

# ---- Certificate ----
doc.add_page_break()
para("B.N.M. Institute of Technology", 14, True, WD_ALIGN_PARAGRAPH.CENTER,
     after=2, spacing=1.0)
para("An Autonomous Institution under VTU", 12, False, WD_ALIGN_PARAGRAPH.CENTER,
     after=2, spacing=1.0)
para("Approved by AICTE, Accredited as grade A Institution by NAAC", 11, False,
     WD_ALIGN_PARAGRAPH.CENTER, after=4, spacing=1.0)
para("Department of Artificial Intelligence and Machine Learning", 12, True,
     WD_ALIGN_PARAGRAPH.CENTER, after=24, spacing=1.0)
para("CERTIFICATE", 18, True, WD_ALIGN_PARAGRAPH.CENTER, after=20, spacing=1.0)
names = ", ".join(f"{n} ({u})" for n, u in TEAM)
para(f"This is to certify that the project work phase – I titled “{TITLE}” carried out by "
     f"{names}, the bonafide students of VII Semester B.E., B.N.M Institute of Technology, in "
     "partial fulfillment for the award of degree in Bachelor of Engineering in ARTIFICIAL "
     "INTELLIGENCE AND MACHINE LEARNING of the Visvesvaraya Technological University, Belagavi "
     f"during the year {YEAR}. This report has been approved as it satisfies the academic "
     "requirements in respect of Project Work Phase – I (23AML175) prescribed for the said "
     "degree.", 12, after=36)
sig = simple_table([["<Guide Name>\n<Designation>\nDept. of AIML\nBNMIT, Bengaluru",
                     "Dr. Sheba Selvam\nProfessor and HOD\nDept. of AIML\nBNMIT, Bengaluru",
                     "Dr. S. Y. Kulkarni\nAdditional Director and Principal\nBNMIT, Bengaluru"]],
                   [2.0, 2.0, 2.0], header_bold=False, size=11)
for row in sig.rows:
    for c in row.cells:
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for b in c._tc.iter(qn("w:tcBorders")):
            pass
sig.style = "Normal Table"
para("", after=0)
para("External Viva", 12, True, WD_ALIGN_PARAGRAPH.LEFT, before=18, after=8, spacing=1.0)
simple_table([["Name of the Examiners", "Signature with Date"],
              ["1.", ""], ["2.", ""]], [3.0, 3.0], size=11)

# ---- Acknowledgement ----
_pre = doc.add_section(WD_SECTION.NEW_PAGE)
margins(_pre)
for _h in (_pre.header, _pre.footer):
    _h.is_linked_to_previous = False
_pf = _pre.footer.paragraphs[0]
_pf.text = ""
_pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
field(_pf, " PAGE ")
set_pgnum(_pre, start=1, fmt="lowerRoman")
para("ACKNOWLEDGEMENT", 18, True, WD_ALIGN_PARAGRAPH.CENTER, after=16, spacing=1.0)
ACK = [
 "The satisfaction and euphoria that accompany the successful completion of any task would be "
 "incomplete without the mention of the people who made it possible, whose constant guidance "
 "and encouragement crowned our effort with success.",
 "We would like to thank Shri Narayan Rao R. Maanay, Secretary, BNMEI, Bengaluru for providing "
 "an excellent academic environment in the College.",
 "We would like to sincerely thank Prof. T. J. Rama Murthy, Director, BNMIT, Bengaluru, for "
 "having extended his support and encouraging us during the course of the work.",
 "We would like to sincerely thank Dr. S. Y. Kulkarni, Additional Director and Principal, "
 "BNMIT, Bengaluru, for having extended his support and encouraging us during the course of "
 "the work.",
 "We would like to express our gratitude to Prof. Eishwar N. Maanay, Dean, BNMIT, Bengaluru "
 "for his relentless support, guidance and assistance.",
 "We would like to thank Dr. Krishnamurthy G. N., Deputy Director, BNMIT, Bengaluru for his "
 "constant encouragement.",
 "We would like to thank Dr. Sheba Selvam, Professor and Head of the Department of Artificial "
 "Intelligence and Machine Learning, BNMIT, Bengaluru, who has shared her opinions and thoughts "
 "which helped us in the completion of our project successfully.",
 "We would also like to thank our Guide <Guide Name>, <Designation>, Department of Artificial "
 "Intelligence and Machine Learning, BNMIT, Bengaluru for guiding us in a systematic manner.",
 "Finally, we would like to thank all technical and non-technical faculty members of the "
 "Department of Artificial Intelligence and Machine Learning, BNMIT, Bengaluru, for their "
 "support. We would like to thank our Family and Friends for their unfailing moral support "
 "and encouragement.",
]
for a in ACK:
    para(a, 12, after=4, spacing=1.25)
para("", after=4, spacing=1.0)
for n, u in TEAM:
    para(f"{n}\t\t{u}", 12, True, WD_ALIGN_PARAGRAPH.RIGHT, after=2, spacing=1.0)

# ---- Table of Contents ----
doc.add_page_break()
para("TABLE OF CONTENTS", 18, True, WD_ALIGN_PARAGRAPH.CENTER, after=14, spacing=1.0)
TOC = [("Certificate", ""), ("Acknowledgement", "i"), ("Table of Contents", "ii"),
       ("List of Figures", "iii"), ("List of Tables", "iii"), ("Abstract", "iv"),
       ("Chapter 1: Introduction", "1"),
       ("        1.1  Motivation", "1"),
       ("        1.2  Problem Statement", "2"),
       ("        1.3  Objectives", "3"),
       ("        1.4  Summary", "3"),
       ("Chapter 2: Literature Survey", "6"),
       ("        2.1  Introduction", "6"),
       ("        2.2  Literature Survey", "6"),
       ("        2.3  Summary", "9"),
       ("Chapter 3: Methodology", "11"),
       ("        3.1  Proposed Approach", "11"),
       ("        3.2  System Architecture", "13"),
       ("References", "16")]
simple_table([["Contents", "Page No."]] + [[a, b] for a, b in TOC], [4.8, 1.2], size=11.5)

# ---- List of Figures / Tables ----
doc.add_page_break()
para("LIST OF FIGURES", 18, True, WD_ALIGN_PARAGRAPH.CENTER, after=14, spacing=1.0)
simple_table([["Sl. No.", "Figure No.", "Name", "Page No."],
              ["1", "Figure 3.1", "High-level system architecture of Saarathi", "14"],
              ["2", "Figure 3.2", "Sequence diagram of one control interval", "15"]],
             [0.7, 1.0, 3.3, 1.0], size=11.5)
para("", after=18)
para("LIST OF TABLES", 18, True, WD_ALIGN_PARAGRAPH.CENTER, before=18, after=14, spacing=1.0)
simple_table([["Sl. No.", "Table No.", "Name", "Page No."],
              ["1", "Table 2.1", "Summary of the literature surveyed", "6"],
              ["2", "Table 3.1", "Passenger Car Unit values used (IRC 106-1990)", "11"],
              ["3", "Table 3.2", "Safety constraints enforced by the safety shell", "12"]],
             [0.7, 1.0, 3.3, 1.0], size=11.5)

# ---- Abstract ----
doc.add_page_break()
para("ABSTRACT", 18, True, WD_ALIGN_PARAGRAPH.CENTER, after=16, spacing=1.0)
para(
 "Traffic signal control determines the delay, the number of stops and the idling emissions of "
 "every vehicle that crosses an intersection. Signals deployed in Indian cities are fixed-time, "
 "vehicle-actuated or rule-based adaptive. Adaptive systems such as the Bengaluru Adaptive "
 "Traffic Control System re-optimise cycle, split and offset using hand-designed rules whose "
 "parameters are calibrated at commissioning and are not revised automatically as demand "
 "patterns change. Reinforcement learning has been studied extensively as an alternative, but "
 "reported controllers are trained and evaluated on the same demand distribution, coordination "
 "and emergency-vehicle priority are developed as separate subsystems, and safety intervals are "
 "expressed as soft penalties rather than enforced constraints.", 12, after=10)
para(
 "This report proposes Saarathi, a decentralised self-learning traffic signal control system. "
 "Every junction runs its own learning agent whose state includes approach-wise demand measured "
 "in Passenger Car Units together with an explicit time-of-day and day-of-week encoding, so that "
 "the agent learns the pattern specific to that junction. On each phase termination the agent "
 "publishes a compact message carrying the released demand, the estimated arrival time at the "
 "neighbouring junction and a priority flag; neighbours use this message to bias their own phase "
 "timing, which produces green waves along a corridor without a central optimiser. The same "
 "message channel carries emergency and escorted-vehicle priority, realised as a priority "
 "corridor with a defined cross-street recovery policy in place of full pre-emption. Every "
 "action produced by the learned policy passes through a non-learned safety shell that enforces "
 "minimum green, maximum green, yellow and all-red intervals, so the safety guarantee is "
 "independent of the training outcome.", 12, after=10)
para(
 "The system is to be modelled on a four-junction Bengaluru corridor in the SUMO microscopic "
 "simulator with the sub-lane model enabled to represent lane-less movement, and evaluated "
 "against fixed-time, vehicle-actuated, max-pressure and rule-based adaptive baselines on "
 "average delay, number of stops, corridor throughput and priority-vehicle travel time, under "
 "both the demand seen during training and demand conditions not seen during training.", 12)

import sys
sys.path.insert(0, str(HERE.parent / "deck"))
from papers import LIT, REFS  # noqa: E402

# ==================================================================== CHAPTER 1
chapter_cover(1, "INTRODUCTION")
chapter_body(restart=1)
heading("CHAPTER 1", 1)
heading("INTRODUCTION", 1)

heading("1.1  Motivation", 2)
para("A signalised intersection is a shared resource. The control logic that allocates green "
     "time at that intersection decides how long each vehicle waits, how many times it is "
     "brought to a stop, and how much fuel it burns while idling. In a city the size of "
     "Bengaluru this allocation is repeated at hundreds of junctions every cycle of every day, "
     "so a small improvement in the control logic accumulates into a large change in total "
     "delay and emissions.")
para("Three families of controllers are in field use. Fixed-time controllers execute a plan "
     "computed offline from historical counts and cannot respond to the demand actually present "
     "at the junction. Vehicle-actuated controllers extend a green interval while a detector "
     "remains occupied, which reacts to one approach at a time and carries no information about "
     "the rest of the network. Adaptive controllers such as SCATS, SCOOT and the indigenous "
     "CoSiCoSt system re-optimise cycle length, phase split and offset online using "
     "hand-designed rules.")
para("Bengaluru has already made the investment required to run the third family. Under the "
     "Bengaluru Adaptive Traffic Control System (BATCS), 155 existing junctions were upgraded "
     "and 14 new junctions were added, giving 169 adaptive signalised junctions in full-scale "
     "operation from April 2025, built on C-DAC's CoSiCoSt controller designed for heterogeneous "
     "traffic. The deployment reports a 33 percent reduction in travel time on the Hudson Circle "
     "corridor and is designed to scale beyond 500 junctions. Camera-based detection and "
     "networked controllers are therefore already installed. Any improvement in the decision "
     "logic can be delivered as a software layer rather than as a new hardware programme.")
para("What that installed base does not do is learn. The parameters of a rule-based adaptive "
     "controller are calibrated by engineers at commissioning. When the demand pattern at a "
     "junction changes — a new flyover opens, a school shifts its timings, a metro station "
     "begins operation — the rules continue to execute with the parameters they were given. "
     "Reinforcement learning offers a control policy learned directly from the traffic the "
     "junction actually observes, and has been studied for signal control for more than a decade "
     "[19], [20]. The motivation for this work is to bring that learning capability to the "
     "infrastructure that already exists, without giving up the safety guarantees that a "
     "deployed signal must provide.")
para("A second motivation is the behaviour of the corridor rather than the junction. Signals "
     "that each optimise in isolation produce a sequence of stops: a vehicle cleared by one "
     "junction arrives at the next during its red interval. Coordinated green waves, in which "
     "neighbouring signals time their greens to receive the platoon released upstream, remove "
     "those stops and reduce both fuel consumption and driver stress. A third motivation is "
     "emergency response. Conventional emergency pre-emption clears the path of an ambulance by "
     "forcing greens along its route, but the delay is transferred to the cross streets and no "
     "recovery behaviour is specified once the vehicle has passed [12].")

heading("1.2  Problem Statement", 2)
para("Deployed adaptive signal controllers optimise using fixed, hand-tuned rules. They do not "
     "learn from the traffic they observe, and their parameters are not revised automatically "
     "when demand patterns shift.")
para("Reported reinforcement learning controllers are trained and tested on the same demand "
     "distribution. Robustness to time-of-day variation, weekday-weekend variation and demand "
     "shift is rarely evaluated, so the behaviour of these controllers under changing field "
     "conditions remains unestablished [1], [4], [6].")
para("Coordination between neighbouring signals and priority for emergency vehicles are studied "
     "as separate problems and would therefore require separate subsystems at deployment "
     "[14], [15], [19], [20]. Emergency priority itself is commonly implemented as full "
     "pre-emption, which clears the priority path but transfers delay to the cross streets with "
     "no defined recovery [12].")
para("Safety intervals are frequently expressed as penalty terms inside the reward function. A "
     "penalty biases the policy but does not guarantee that a minimum green or an all-red "
     "clearance interval is respected, particularly during exploration [9].")
para("The problem addressed in this work is therefore to design a traffic signal control system "
     "that learns the demand pattern specific to each junction, sustains that performance as the "
     "pattern changes, and delivers corridor coordination and emergency priority through a single "
     "mechanism, while safety intervals are enforced outside the learned policy.", bold=False)

heading("1.3  Objectives", 2)
OBJ = [
 "To model a four-junction Bengaluru corridor in the SUMO microscopic simulator using the "
 "sub-lane model, with heterogeneous PCU-weighted demand and a 24-hour time-of-day profile.",
 "To design a per-junction reinforcement learning agent whose state includes approach-wise PCU "
 "occupancy together with an explicit time-of-day and day-of-week encoding.",
 "To implement a non-learned safety shell that enforces minimum green, maximum green, yellow "
 "and all-red intervals on every action issued by the agent.",
 "To implement neighbour-to-neighbour platoon messaging carrying released PCU, estimated "
 "arrival time and a priority flag, so that green waves form without a central controller.",
 "To realise emergency and escorted-vehicle priority on the same messaging channel as a "
 "priority corridor with a defined cross-street recovery policy, in place of full pre-emption.",
 "To establish a continual learning loop in which the policy is periodically retrained and "
 "validated on a simulation twin before any updated policy is accepted.",
 "To evaluate the system against fixed-time, vehicle-actuated, max-pressure and rule-based "
 "adaptive baselines on delay, stops, throughput and priority-vehicle travel time, including "
 "demand conditions not seen during training.",
]
for i, o in enumerate(OBJ, 1):
    para(f"{i}.  {o}", 12, after=6)

heading("1.4  Summary", 2)
para("This chapter has set out why traffic signal control in Bengaluru is a problem worth "
     "addressing in software rather than in hardware, and why a learning controller is the "
     "natural next step for an installed base of adaptive signals. The problem statement "
     "identifies four specific shortcomings in current practice: the absence of learning in "
     "deployed adaptive control, the absence of any evaluation of generalisation in reported "
     "learning control, the separation of coordination from priority handling, and the "
     "treatment of safety as a penalty rather than a constraint. Seven objectives follow from "
     "these shortcomings. The next chapter surveys the literature that establishes them.")

# ==================================================================== CHAPTER 2
chapter_cover(2, "LITERATURE SURVEY")
chapter_body()
heading("CHAPTER 2", 1)
heading("LITERATURE SURVEY", 1)

heading("2.1  Introduction", 2)
para("Twenty journal and conference papers published between 2019 and 2026 were surveyed, "
     "selected to cover four themes relevant to this work: the formulation of signal control as "
     "a reinforcement learning problem, cooperation between neighbouring signals, emergency "
     "vehicle priority, and the robustness of learned controllers to conditions not seen during "
     "training. Papers dealing with Indian heterogeneous traffic were included specifically "
     "because standard benchmarks assume lane discipline. The papers are listed in descending "
     "order of year of publication in Table 2.1, with the methodology used and the drawbacks "
     "identified in each.")

heading("2.2  Literature Survey", 2)
para("Table 2.1: Summary of the literature surveyed", 11, True,
     WD_ALIGN_PARAGRAPH.CENTER, after=6, spacing=1.0)
rows = [["Sl. No.", "Paper Title, Author, Publication details",
         "Methodology Used", "Drawbacks"]]
for i, (t, m, d) in enumerate(LIT, 1):
    rows.append([str(i), t, m, d])
simple_table(rows, [0.45, 2.15, 1.75, 1.65], size=9)

para("", after=10)
para("The surveyed work groups into four themes.", 12, after=6)
para("Formulation and single-junction control. Papers [4] to [8] establish the standard "
     "formulation: the state is an encoding of queue or pressure on each approach, the action "
     "selects or extends a phase, and the reward is the negative of a delay or queue measure. "
     "Hierarchical decomposition [7] reduces the effective action space, and multi-objective "
     "formulations [8], [16] optimise delay, queue length and emissions jointly. In all of these "
     "the objective weights or the reward shaping are fixed by hand and do not adapt when the "
     "demand pattern changes.")
para("Cooperation between junctions. CoLight [20] applies graph attention so that each junction "
     "weights the influence of its neighbours, and MA2C [19] uses decentralised advantage "
     "actor-critic with neighbour state sharing and spatial reward discounting. Learned "
     "communication [14] compresses the neighbour signal further. These methods demonstrate "
     "that coordination improves corridor performance, but they require a jointly trained "
     "network-wide model: a single junction cannot be retrained without retraining its "
     "neighbours, and the content of a learned message cannot be audited by an operator.")
para("Emergency vehicle priority. EMVLight [15] learns emergency-vehicle routing together with "
     "signal control and reduces response time, but assumes control over the route of the "
     "vehicle. Chen et al. [12] quantify the delay that conventional pre-emption imposes on "
     "cross traffic and propose spillback-aware timing, but the method is rule-based, applies to "
     "a single corridor, and is not integrated with a learning controller.")
para("Robustness and Indian conditions. The 2026 robustness studies [1], [3] stress-test trained "
     "controllers under demand surges, detector faults and incidents, and report that "
     "performance degrades once the operating conditions differ from those seen during training; "
     "neither proposes a controller that retains performance. The 2025 surveys [4], [6] name "
     "generalisation across time-of-day and demand regimes as an open problem. Continual "
     "reinforcement learning [10] offers the machinery to keep learning under non-stationary "
     "conditions, but has not been instantiated as a deployment procedure for signal control. "
     "For Indian traffic, [11] combines max-pressure with reinforcement learning using PCU-based "
     "demand for lane-less streams but controls junctions independently, and [17] compares "
     "classical controllers on Bengaluru junction data without any learning component. The "
     "widely used benchmark library [13] contains only lane-based scenarios.")

heading("2.3  Summary", 2)
para("The survey identifies six gaps. First, generalisation is not evaluated: controllers are "
     "trained and tested on the same demand distribution [1], [4], [6]. Second, non-stationarity "
     "is not handled operationally; continual learning exists in the general literature but not "
     "as a retrain-validate-deploy procedure for signals [10]. Third, safety is penalised rather "
     "than enforced, so clearance intervals can be violated during exploration [9]. Fourth, "
     "coordination [14], [19], [20] and emergency priority [12], [15] are developed as separate "
     "mechanisms. Fifth, pre-emption has no defined recovery for the cross streets [12]. Sixth, "
     "Indian heterogeneous lane-less traffic is under-represented: standard benchmarks are "
     "lane-based [13], and the PCU-based studies that do address it control junctions in "
     "isolation [11], [17]. The methodology proposed in the next chapter addresses these six "
     "gaps directly.")

# ==================================================================== CHAPTER 3
chapter_cover(3, "METHODOLOGY")
chapter_body()
heading("CHAPTER 3", 1)
heading("METHODOLOGY", 1)

heading("3.1  Proposed Approach", 2)
heading("3.1.1  Model chosen", 3)
para("Signal control at a single junction is formulated as a Markov decision process and solved "
     "with Proximal Policy Optimisation (PPO), an on-policy policy-gradient algorithm. One agent "
     "is instantiated per junction; no agent has access to the state of the whole network.")
para("State. The observation supplied to the agent at each decision instant consists of the "
     "approach-wise demand measured in Passenger Car Units, a one-hot encoding of the current "
     "phase, the time elapsed in that phase, a sine-cosine encoding of the time of day, a binary "
     "weekday flag, and the most recent message received from each neighbouring junction. The "
     "time encoding is what allows one agent to learn distinct behaviour for the morning peak, "
     "the afternoon lull and the evening peak at its own junction rather than an average of all "
     "three.")
para("Demand is expressed in Passenger Car Units because Indian traffic is heterogeneous and "
     "lane-less: two-wheelers, autorickshaws, cars, buses and trucks share the same carriageway "
     "and a raw vehicle count does not represent the capacity consumed. The conversion factors "
     "used are those of IRC 106-1990, listed in Table 3.1.")
para("Table 3.1: Passenger Car Unit values used (IRC 106-1990)", 11, True,
     WD_ALIGN_PARAGRAPH.CENTER, before=8, after=6, spacing=1.0)
simple_table([["Vehicle type", "Two-wheeler", "Autorickshaw", "Car", "Bus", "Truck"],
              ["PCU value", "0.5", "1.2", "1.0", "3.0", "3.0"]],
             [1.15, 1.0, 1.45, 0.66, 0.66, 0.66], size=11)
para("", after=8)
para("Action. At each decision instant the agent chooses between holding the current phase and "
     "advancing to the next phase in a fixed cyclic order. Decisions are taken every 5 seconds. "
     "Restricting the action to this binary choice keeps the action space small and keeps the "
     "phase order predictable to drivers.")
para("Reward. The reward is the negative PCU-weighted delay accumulated over the decision "
     "interval, with a small penalty applied whenever the agent switches phase. The switching "
     "penalty prevents the degenerate policy of changing phase at every opportunity, which would "
     "maximise the instantaneous queue reduction while making the junction unusable.")
para("Safety shell. The action selected by the policy is not sent to the controller directly. It "
     "passes through a non-learned wrapper that clamps it to the constraints listed in Table 3.2. "
     "A switch requested before the minimum green has elapsed is suppressed; a hold requested "
     "after the maximum green has elapsed is overridden; every phase change is followed by the "
     "yellow and all-red intervals. Because the shell is a fixed program and not a learned "
     "component, these guarantees hold during training, during exploration and after any "
     "subsequent retraining.")
para("Table 3.2: Safety constraints enforced by the safety shell", 11, True,
     WD_ALIGN_PARAGRAPH.CENTER, before=8, after=6, spacing=1.0)
simple_table([["Constraint", "Value", "Effect"],
              ["Minimum green", "10 s", "A switch requested earlier is suppressed"],
              ["Maximum green", "60 s", "A hold requested later is overridden"],
              ["Yellow interval", "3 s", "Inserted on every phase change"],
              ["All-red interval", "2 s", "Inserted after every yellow interval"],
              ["Decision interval", "5 s", "Period at which the policy is queried"]],
             [1.5, 0.8, 3.7], size=11)
para("", after=8)
para("Coordination. When a phase terminates, the agent publishes a message to its neighbours "
     "containing three fields: the demand released in PCU, the estimated time at which that "
     "platoon will arrive at the neighbouring junction, and a priority flag. A receiving agent "
     "treats the message as part of its state and biases its own phase timing to be green when "
     "the platoon arrives. Coordination therefore emerges from local decisions and an explicit, "
     "readable message, with no central optimiser and no jointly trained network model.")
para("Priority corridor. The same message carries emergency and escorted-vehicle priority. A "
     "priority flag of 1 denotes an ambulance and 2 an escorted convoy; a higher flag raises the "
     "precedence of the message along the route, so that successive junctions prepare a green "
     "corridor ahead of the vehicle instead of the road being closed to all other traffic. The "
     "safety shell remains in force throughout, and once the priority vehicle has passed, a "
     "recovery policy returns extended service to the approaches that were held, so that the "
     "delay imposed on the cross streets is repaid rather than left unaccounted.")
para("Continual learning. The policy is retrained periodically on recently logged demand inside "
     "a simulation twin of the junction. A retrained policy is deployed only if it validates "
     "above the incumbent policy on held-out demand. This makes adaptation to a changed demand "
     "pattern an operational procedure with a decision gate, rather than a property assumed of "
     "the learning algorithm.")

heading("3.1.2  Reason for choosing the model", 3)
para("PPO is stable on small discrete action spaces and, being on-policy, avoids the replay "
     "buffer tuning that value-based methods require when the demand distribution is "
     "non-stationary. Its clipped objective bounds the size of each policy update, which matters "
     "for a controller that is retrained repeatedly against a live demand log.")
para("A per-junction agent avoids the joint action-space growth of centralised multi-agent "
     "control, whose size is exponential in the number of junctions, and it allows a single "
     "junction to be retrained or replaced without retraining the corridor — a practical "
     "requirement that jointly trained models such as [20] do not satisfy.")
para("A PCU-based state matches what camera-based detection at Indian junctions can actually "
     "supply. No per-class vehicle classification is assumed, so the sensing requirement is met "
     "by the equipment already installed under BATCS.")
para("Enforcing the safety intervals outside the learned policy keeps the guarantee independent "
     "of the training outcome. In soft-penalty formulations [9] the constraint competes with the "
     "delay term in the reward and can be traded away; here it cannot be.")

heading("3.2  System Architecture", 2)
para("Figure 3.1 shows the high-level architecture of the system at one junction. Every junction "
     "in the corridor runs an identical stack.")
figure(IMG / "arch.png", "Figure 3.1: High-level system architecture of Saarathi")
para("Detection at the junction supplies a raw mixed vehicle stream, which the PCU estimator "
     "converts into approach-wise demand in Passenger Car Units. A priority beacon carried by an "
     "ambulance or an escort vehicle enters the same estimator as a priority flag. The junction "
     "agent receives this demand together with the current phase, the time elapsed in the phase, "
     "the time-of-day and weekday encoding, and the latest neighbour message, and produces an "
     "action. The action passes through the safety shell, which clamps it to the constraints of "
     "Table 3.2 before it reaches the signal controller. In parallel, the agent publishes its "
     "platoon message to the neighbour message bus, from which the adjacent junction agents read "
     "it. The nightly simulation twin consumes the logged demand, retrains the policy and applies "
     "the deploy gate.")
para("Figure 3.2 shows the sequence of messages exchanged during one control interval, including "
     "the case in which a priority vehicle is detected.")
figure(IMG / "seq.png", "Figure 3.2: Sequence diagram of one control interval")
para("In the routine case, the PCU estimator supplies the state, the agent proposes an action, "
     "the safety shell validates it and issues the phase command, and the controller reports the "
     "realised phase back to the agent. The agent then publishes the platoon message with "
     "priority 0 to its neighbour. When a priority vehicle is detected, the estimator raises the "
     "priority flag, the agent issues a priority corridor request carrying the estimated arrival "
     "time and the priority level, and the neighbour acknowledges by applying the corresponding "
     "offset. The agent requests an extension of green on the priority approach; the safety shell "
     "still issues that command within the minimum and maximum green limits rather than holding "
     "the phase indefinitely. Once the vehicle has cleared, the agent signals the end of the "
     "priority corridor and the cross-street recovery policy takes effect.")
para("The evaluation of this design will compare it against fixed-time, vehicle-actuated, "
     "max-pressure and rule-based adaptive controllers on average delay per vehicle, number of "
     "stops, corridor throughput and priority-vehicle travel time, measured both on the demand "
     "seen during training and on demand conditions constructed by shifting the time-of-day "
     "profile and the total demand level.")

# =================================================================== REFERENCES
doc.add_page_break()
heading("REFERENCES", 1)
for i, r in enumerate(REFS, 1):
    para(f"[{i}]  {r}", 12, after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY, spacing=1.15)

doc.save(str(OUT))
print("saved", OUT)
