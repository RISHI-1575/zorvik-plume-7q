#!/usr/bin/env python
"""Saarathi Phase-I report v2, built on the college template (fmt1.docx).
Usage: build_report2.py [pages.json]   (pages.json = page numbers from a first pass)"""
import copy, json, re, sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.section import WD_SECTION
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = Path(__file__).resolve().parent
TEMPLATE = Path("/Users/rishi/Downloads/1. Format - Project Phase 1 Report.docx")
FIG = HERE / "fig2"
OUT = HERE / "Saarathi_Front_Matter.docx"
OUT_BODY = HERE / "Saarathi_Project_Report.docx"
PAGES = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else {}

TITLE = ("Saarathi: A Self-Learning Decentralised Traffic Signal Control System "
         "with Coordinated Green Waves and Emergency Priority Corridors")
SHORT = "Saarathi: Self-Learning Decentralised Traffic Signal Control"
TEAM = [("P Yukthesh", "1BG23AI068"), ("Rishi Shashikanth", "1BG23AI083"),
        ("Vimal", "1BG24AI411")]
GUIDE, GUIDE_DES = "<Guide Name>", "<Designation>"
TNR = "Times New Roman"
J, C, L = WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT
TEXTW = 5.77

doc = Document(str(TEMPLATE))
body = list(doc.element.body.iterchildren())
P = lambda i: Paragraph(body[i], doc)


def tnr(r):
    rpr = r.get_or_add_rPr()
    f = rpr.find(qn("w:rFonts"))
    if f is None:
        f = OxmlElement("w:rFonts"); rpr.insert(0, f)
    for a in ("ascii", "hAnsi", "cs", "eastAsia"):
        f.set(qn("w:" + a), TNR)
    for a in ("asciiTheme", "hAnsiTheme", "cstheme", "eastAsiaTheme"):
        f.attrib.pop(qn("w:" + a), None)


def retext(p, parts):
    """Replace a template paragraph's text, keeping its first run's look.
    parts: str or list of (text, bold); '\n' inside text becomes a line break."""
    if isinstance(parts, str):
        parts = [(parts, None)]
    runs = p.runs
    proto = copy.deepcopy(runs[0]._r)
    for r in runs:
        r._r.getparent().remove(r._r)
    for text, bold in parts:
        r = copy.deepcopy(proto)
        for t in r.findall(qn("w:t")) + r.findall(qn("w:br")):
            r.remove(t)
        p._p.append(r)
        run = p.runs[-1]
        for k, line in enumerate(text.split("\n")):
            if k:
                run.add_break()
            run.add_text(line)
        if bold is not None:
            run.bold = bold


# ================================================= front matter from template
# Cover (s0)
retext(P(16), TITLE.upper())
P(16).runs[0].font.color.rgb = RGBColor(0x1F, 0x3A, 0x93)
cover_team = []
for k, (n, u) in enumerate(TEAM):
    cover_team += [(n + " ", True), (f"({u})" + ("\n" if k < len(TEAM) - 1 else ""), False)]
retext(P(19), cover_team)
P(19).alignment = C
for i in (19, 77):
    pf = P(i).paragraph_format
    pf.left_indent = pf.right_indent = pf.first_line_indent = Inches(0)
retext(P(24), f"{GUIDE}\n{GUIDE_DES}")

# Certificate (s1)
names = ", ".join(f"{n} ({u})" for n, u in TEAM[:-1]) + f" and {TEAM[-1][0]} ({TEAM[-1][1]})"
retext(P(42), [("This is to certify that the project work phase – I titled ", False),
               (TITLE + " ", True), ("carried out by ", False), (names + ", ", True),
               ("the bonafide students of VII Semester B.E., ", False)])
retext(P(43), [("B.N.M Institute of Technology, ", True),
               ("in partial fulfillment for the award of degree in ", False),
               ("Bachelor of Engineering ", True),
               ("in Artificial Intelligence and Machine Learning of the ", False),
               ("Visvesvaraya Technological University", True),
               (", Belagavi during the year 2026-27. This report has been approved as it "
                "satisfies the academic requirements in respect of Project Work Phase – I "
                "(23AML175) prescribed for the said degree.", False)])
sig = Table(body[53], doc).cell(0, 0).paragraphs
retext(sig[0], [(GUIDE, True), (f"\n{GUIDE_DES}\nDept. of AIML", False)])

# Acknowledgement (s2)
ACK = {
    57: [("Any piece of work that runs over a full semester depends on more people than "
          "the ones whose names appear on the cover. We would like to record our thanks to "
          "those who helped us reach this stage of the project.", None)],
    59: [("We thank ", False), ("Shri Narayan Rao R. Maanay, ", True),
         ("Secretary, BNMEI, Bengaluru, for the academic environment and facilities that "
          "the college provides.", False)],
    61: [("We sincerely thank ", False), ("Prof. T. J. Rama Murthy, ", True),
         ("Director, BNMIT, Bengaluru, for his support and encouragement.", False)],
    63: [("We sincerely thank ", False), ("Dr. S.Y. Kulkarni, ", True),
         ("Additional Director and Principal, BNMIT, Bengaluru, for giving us the "
          "opportunity to take up this project.", False)],
    65: [("We express our gratitude to ", False), ("Prof. Eishwar N. Maanay, ", True),
         ("Dean, BNMIT, Bengaluru, for his constant support.", False)],
    67: [("We thank ", False), ("Dr. Krishnamurthy G.N, ", True),
         ("Deputy Director, BNMIT, Bengaluru, for his encouragement.", False)],
    69: [("We thank ", False), ("Dr. Sheba Selvam, ", True),
         ("Professor and Head of the Department of Artificial Intelligence and Machine "
          "Learning, BNMIT, Bengaluru, for her support and for the review process that kept "
          "the project on schedule.", False)],
    71: [("We are grateful to our guide ", False), (GUIDE + ", ", True),
         (GUIDE_DES + ", ", True),
         ("Department of Artificial Intelligence and Machine Learning, BNMIT, Bengaluru, "
          "who listened patiently to our early ideas, questioned the weak ones and helped "
          "us shape the rest into a plan we can actually carry out.", False)],
    73: [("Finally, we thank the teaching and non-teaching staff of the Department of "
          "Artificial Intelligence and Machine Learning, BNMIT, for their help, and our "
          "families and friends for putting up with long evenings spent watching simulated "
          "traffic.", None)],
}
for i, parts in ACK.items():
    retext(P(i), parts)
retext(P(77), "\n".join(f"{n} ({u})" for n, u in TEAM))
P(77).alignment = WD_ALIGN_PARAGRAPH.RIGHT

# make every existing run Times New Roman (cover used English111 Vivace BT)
for part in [doc.part] + [s.footer.part for s in doc.sections[2:3]]:
    for r in part.element.iter(qn("w:r")):
        tnr(r)
def tnr_doc(d, normal=False):
    """Force Times New Roman on every style and on the document defaults."""
    for st in d.styles:
        if st.type == 1 and st.element.rPr is not None:
            f = st.element.rPr.find(qn("w:rFonts"))
            if f is not None:
                for a in ("ascii", "hAnsi", "cs", "eastAsia"):
                    f.set(qn("w:" + a), TNR)
    dd = d.styles.element.find(qn("w:docDefaults"))
    f = dd.find(".//" + qn("w:rFonts"))
    for a in ("ascii", "hAnsi", "cs", "eastAsia"):
        f.set(qn("w:" + a), TNR)
    for a in ("asciiTheme", "hAnsiTheme", "cstheme", "eastAsiaTheme"):
        f.attrib.pop(qn("w:" + a), None)
    if normal:
        n = d.styles["Normal"]
        n.font.size = Pt(12)
        n.paragraph_format.line_spacing = 1.5
        n.paragraph_format.space_after = Pt(8)


tnr_doc(doc)


# ================================================= helpers for new content
def run(p, text, size=12, bold=False, italic=False, sub=False, sup=False):
    r = p.add_run(text)
    tnr(r._r)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    r.font.subscript = sub or None; r.font.superscript = sup or None
    return r


def para(text="", size=12, bold=False, align=J, before=0, after=8, spacing=1.5,
         italic=False):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after); pf.line_spacing = spacing
    pf.first_line_indent = None
    if text:
        rich(p, text, size, bold, italic)
    return p


def rich(p, text, size=12, bold=False, italic=False):
    """*italic* and **bold** markup inside body text."""
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|_\{[^}]*\}|\^\{[^}]*\})", text):
        if tok.startswith("_{") or tok.startswith("^{"):
            run(p, tok[2:-1], size, bold, True, sub=tok[0] == "_", sup=tok[0] == "^")
        elif tok.startswith("**"):
            run(p, tok[2:-2], size, True, italic)
        elif tok.startswith("*"):
            run(p, tok[1:-1], size, bold, True)
        elif tok:
            run(p, tok, size, bold, italic)


def bullets(items, numbered=False):
    for k, it in enumerate(items, 1):
        p = para(after=3)
        p.paragraph_format.left_indent = Inches(0.35)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        if numbered:
            rich(p, f"{k}.\t" + it)
        else:
            m = run(p, "\uF0B7\t")
            m._r.rPr.find(qn("w:rFonts")).set(qn("w:ascii"), "Symbol")
            m._r.rPr.find(qn("w:rFonts")).set(qn("w:hAnsi"), "Symbol")
            rich(p, it)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(0.35))


def move_before(el, anchor):
    anchor.addprevious(el)


def set_pgnum(sec, start=None):
    sp = sec._sectPr
    pg = sp.find(qn("w:pgNumType"))
    if pg is not None:
        sp.remove(pg)
    if start is not None:
        pg = OxmlElement("w:pgNumType"); pg.set(qn("w:start"), str(start))
        pg.set(qn("w:fmt"), "decimal")
        sp.append(pg)


def a4(sec):
    """Body-document page setup, as in the department format: 8.5 x 11 in,
    1.5 in binding margin, 1 in elsewhere."""
    sec.page_width, sec.page_height = Inches(8.5), Inches(11.0)
    sec.left_margin = Inches(1.5)
    sec.right_margin = sec.top_margin = sec.bottom_margin = Inches(1.0)
    sec.header_distance = Inches(0.6)
    sec.footer_distance = Inches(0.4)


def field(p, code, size=12):
    r = p.add_run(); tnr(r._r); r.font.size = Pt(size)
    for kind, txt in (("begin", None), (None, code), ("end", None)):
        if kind:
            e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), kind)
        else:
            e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt
        r._r.append(e)


def clear_hf(sec):
    for h in (sec.header, sec.footer):
        h.is_linked_to_previous = False
        for p in h.paragraphs:
            p.text = ""


def rule(p, side):
    """Thick-thin rule above the footer / below the header, as in the format."""
    bdr = OxmlElement("w:pBdr"); e = OxmlElement("w:" + side)
    for k, v in (("val", "thickThinSmallGap"), ("sz", "24"), ("space", "1"),
                 ("color", "auto")):
        e.set(qn("w:" + k), v)
    bdr.append(e); p._p.get_or_add_pPr().append(bdr)


def chapter(num, name, restart=None):
    """Chapter opening: CHAPTER n on the left, the chapter name centred below it,
    with the text of the chapter following on the same page."""
    sec = doc.sections[0] if not doc.paragraphs else doc.add_section(WD_SECTION.NEW_PAGE)
    a4(sec); clear_hf(sec); set_pgnum(sec, restart)
    hp = sec.header.paragraphs[0]; hp.alignment = L
    hp.paragraph_format.space_after = Pt(0)
    hp.paragraph_format.line_spacing = 1.0
    run(hp, SHORT, 12)
    rule(hp, "bottom")
    fp = sec.footer.paragraphs[0]
    fp.paragraph_format.space_after = Pt(0)
    fp.paragraph_format.line_spacing = 1.0
    rule(fp, "top")
    ts = fp.paragraph_format.tab_stops
    for pos in (4680, 9360):            # drop the tab stops inherited from the style
        clr = OxmlElement("w:tab")
        clr.set(qn("w:val"), "clear"); clr.set(qn("w:pos"), str(pos))
        ts._pPr.get_or_add_tabs().append(clr)
    ts.add_tab_stop(Inches(TEXTW / 2), WD_TAB_ALIGNMENT.CENTER)
    ts.add_tab_stop(Inches(TEXTW), WD_TAB_ALIGNMENT.RIGHT)
    run(fp, "B.E/Dept.of AIML/BNMIT\t", 12)
    field(fp, " PAGE ", 12)
    run(fp, "\t2026-2027", 12)
    para(f"CHAPTER {num}", 18, True, L, after=6, spacing=1.5)
    para(name.upper(), 16, True, C, after=10, spacing=1.5)


def heading(text, level):
    size = {1: 18, 2: 14, 3: 12, 4: 12}[level]
    p = para(text, size, True, L, before=8 if level > 1 else 0, after=6, spacing=1.5)
    p.paragraph_format.keep_with_next = True
    return p


FIGS, TABS = [], []


def figure(name, caption, width=None):
    p = para(align=C, before=6, after=4, spacing=1.0)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(FIG / name), width=Inches(width or TEXTW - 0.2))
    para(caption, 12, False, C, after=12, spacing=1.0)
    FIGS.append(caption)


def table(caption, rows, widths, size=11, align0=True):
    cp = para(caption, 12, True, L, before=6, after=6, spacing=1.0)
    cp.paragraph_format.keep_with_next = True
    TABS.append(caption)
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    brd = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + side)
        for k, v in (("val", "single"), ("sz", "4"), ("space", "0"), ("color", "000000")):
            e.set(qn("w:" + k), v)
        brd.append(e)
    t._tbl.tblPr.append(brd)
    t.alignment = 1
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(lay)
    hdr = OxmlElement("w:tblHeader")        # repeat the header row on each page
    t.rows[0]._tr.get_or_add_trPr().append(hdr)
    k = TEXTW / sum(widths)
    for j, w in enumerate(widths):
        t.columns[j].width = Inches(w * k)
    for i, row in enumerate(rows):
        for j, txt in enumerate(row):
            c = t.cell(i, j); c.width = Inches(widths[j] * k)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            p.alignment = C if (i == 0 or (j == 0 and align0)) else L
            run(p, txt, size, bold=(i == 0))
    para(after=6, spacing=1.0)


def eq(text, num):
    """Centred equation, number right-justified. _{x} subscript, ^{x} superscript."""
    p = para(align=L, before=4, after=8, spacing=1.15)
    ts = p.paragraph_format.tab_stops
    ts.add_tab_stop(Inches(TEXTW / 2), WD_TAB_ALIGNMENT.CENTER)
    ts.add_tab_stop(Inches(TEXTW), WD_TAB_ALIGNMENT.RIGHT)
    run(p, "\t")
    for tok in re.split(r"(_\{[^}]*\}|\^\{[^}]*\})", text):
        if tok.startswith("_{"):
            run(p, tok[2:-1], italic=True, sub=True)
        elif tok.startswith("^{"):
            run(p, tok[2:-1], italic=True, sup=True)
        elif tok:
            run(p, tok, italic=True)
    run(p, f"\t({num})")


def text(*paras):
    for t in paras:
        para(t)


# ================================================= LoF / LoT (filled after body)
def fill_list(tbl_el, items, pages):
    t = Table(tbl_el, doc)
    while len(t.rows) < len(items) + 1:
        t._tbl.append(copy.deepcopy(t.rows[-1]._tr))
    for k, cap in enumerate(items, 1):
        num, name = cap.split(" ", 2)[1].rstrip(":"), cap.split(" ", 2)[2]
        for c, v in zip(t.rows[k].cells, (num, name, str(pages.get(cap, "")))):
            c.paragraphs[0].text = ""
            for extra in c.paragraphs[1:]:
                extra._p.getparent().remove(extra._p)
            run(c.paragraphs[0], v, 12)
            c.paragraphs[0].alignment = L if v == name else C


# ================================================= ABSTRACT
ABSTRACT = [
    "Signal controllers that learn from traffic have been studied for over two decades, but "
    "almost all of them are trained and tested on lane-disciplined traffic of the kind found "
    "in Europe, North America and China. A typical Bengaluru junction looks very different. "
    "Two-wheelers make up close to half the stream, they do not stay in lanes, and an "
    "auto-rickshaw, a car and a city bus waiting at the same stop line load the junction in "
    "very different amounts. Counting each of them as one vehicle, which is what most "
    "published controllers do, hides the real demand.",
    "This report describes Phase I of Saarathi, a project with two outcomes. The first is an "
    "open simulation environment for non-lane mixed traffic, built on the sublane model of "
    "SUMO with five Indian vehicle classes, lateral filtering by two-wheelers and "
    "auto-rickshaws, and demand weighted in passenger car units (PCU) following IRC:106-1990. "
    "The second is a decentralised controller in which a Proximal Policy Optimisation (PPO) "
    "agent runs at each junction of a four-junction arterial corridor. Each agent reads PCU "
    "queues rather than vehicle counts, exchanges short messages with its neighbours so that "
    "green waves can form, gives ambulances a priority corridor and is held inside a fixed "
    "safety shell of minimum green, maximum green, yellow and all-red times. The agents are "
    "retrained each night on the previous day's demand. We also define a cross-street "
    "recovery time, which measures how long the side streets take to return to normal after "
    "an ambulance has passed.",
    "In the work done so far, the corridor and the vehicle models are complete and two "
    "baselines have been run. In a one-hour morning-peak scenario, fixed-time control gave an "
    "average delay of 66.5 s per vehicle and Max Pressure gave 46.4 s. These numbers form the "
    "reference against which the learning controller, MPLight and CoLight will be compared "
    "in Phase II, together with ambulance travel time, cross-street recovery time and delay "
    "for each vehicle class.",
]
# front matter order: Acknowledgement (i), Abstract, Table of Contents,
# List of Figures, List of Tables.  The template's "List of Figures" section is
# reused for the abstract; the lists are rebuilt at the end of the run.
retext(P(79), "ABSTRACT")
for idx in (80, 81, 82, 83, 84):
    body[idx].getparent().remove(body[idx])
for t in ABSTRACT:
    move_before(para(t, after=8)._p, body[85])

# ================================================= body document
front = doc
doc = Document()
tnr_doc(doc, normal=True)
TEXTW = 6.0

# ================================================= CHAPTER 1
chapter(1, "Introduction", restart=1)
text(
    "Anyone who has waited at Silk Board or Hebbal during the morning rush knows that a "
    "traffic signal can either keep a junction moving or make a bad situation worse. Most "
    "signals in Indian cities still run on fixed plans. A plan is worked out once from a "
    "traffic survey, a green time is assigned to each approach, and the same cycle repeats "
    "until somebody changes it by hand. When the traffic on the day matches the survey, "
    "this works well enough. When it does not, which is most of the time, one approach sits "
    "on a red light facing an empty crossing road while the queue on another grows back "
    "into the previous junction.",
    "Adaptive control tries to fix this by measuring traffic and changing the timings as it "
    "goes. Systems such as SCATS [2] and RHODES [3] have done this for decades using loop "
    "detectors and hand-built optimisation rules. In the last ten years the research focus "
    "has moved to reinforcement learning (RL), where the controller is an agent that learns "
    "a timing policy by trial and error in a simulator instead of being told the rules "
    "[11], [13]. The results reported in the literature are encouraging, but they come with "
    "an assumption that is rarely stated: the traffic follows lanes, and every vehicle "
    "counts the same.",
    "Indian traffic breaks both halves of that assumption. This project, Saarathi, starts "
    "from that gap. It builds a simulation environment in which Indian mixed traffic "
    "behaves the way it does on the road, puts a learning controller at each junction of a "
    "short corridor, and then tests that controller against the best-known alternatives on "
    "equal terms. This chapter explains why the work is needed, states the problem and lists "
    "the objectives.",
)
heading("1.1 Motivation", 2)
text(
    "Three observations pushed us towards this project.",
    "**Mixed traffic is the normal case, not an exception.** In our corridor model, which "
    "uses a Bengaluru-like modal split, two-wheelers are 44.6 per cent of all vehicles but "
    "only 18.9 per cent of the load once each vehicle is weighted by its PCU value. Buses "
    "are the reverse: 8.2 per cent of vehicles but 20.8 per cent of the load. Figure 1.1 "
    "shows this for all five classes. A controller that counts heads will over-serve an "
    "approach full of motorcycles and under-serve one holding two buses and a truck. The "
    "PCU values themselves are not our invention. They come from the Indian Roads Congress "
    "guideline IRC:106-1990 [29], and the idea that equivalence factors change with the "
    "traffic mix and the road width has been studied closely by Indian researchers [21], "
    "[26].",
)
figure("share.png", "Figure 1.1: Share of vehicles versus share of PCU load for each class "
       "in the simulated corridor", width=5.2)
text(
    "**Vehicles do not stay in lanes.** Two-wheelers and auto-rickshaws move sideways into "
    "any gap wide enough for them and collect at the front of the queue during red. Our "
    "environment reproduces this with SUMO's sublane model at a lateral resolution of "
    "0.4 m, giving the two small classes free lateral alignment while cars, buses and "
    "trucks hold the lane centre. Arasan and Koshy [22] and "
    "Asaithambi et al. [25] explain why lane-based car-following models do not describe "
    "this behaviour, and trajectory data collected in Chennai by Kanagaraj et al. [24] "
    "confirm it. Almost all public benchmarks for learning signal controllers, however, "
    "are built on lane-based simulators and city networks from outside India [11], [14].",
    "**Real deployments are starting, but they do not learn.** Bengaluru has begun "
    "upgrading junctions to camera-based adaptive control. Such systems adjust timings from "
    "measured queues using fixed rules, much like SCATS [2]. They do not improve with "
    "experience, and there is no public way to check how any controller, rule-based or "
    "learned, would behave on Indian traffic before it is installed at a junction. An open "
    "environment would let researchers and city engineers try ideas on a screen before "
    "trying them on a road.",
    "Emergency vehicles add a further concern. Clearing a path for an ambulance is easy to "
    "promise and hard to do well, because every green given to the ambulance's route is a "
    "red for someone else. Studies such as EMVLight [17] measure how much faster the "
    "ambulance arrives. Few measure how long the cross streets take to recover afterwards, "
    "and in a dense Indian corridor that recovery can matter as much as the ambulance "
    "itself.",
)
heading("1.2 Problem Statement", 2)
text(
    "Existing learning-based traffic signal controllers are designed and evaluated on "
    "lane-disciplined traffic in which every vehicle is counted as one unit. There is no "
    "open simulation environment that reproduces Indian non-lane mixed traffic, and so "
    "nobody can say how well these controllers, or simpler ones such as Max Pressure, work "
    "on Indian roads. There is also no controller that together (i) senses load in PCU, "
    "(ii) coordinates with neighbouring junctions to form green waves, (iii) gives "
    "emergency vehicles priority and measures the cost of that priority to the cross "
    "streets, and (iv) stays within safe signal timings while continuing to adapt as "
    "demand changes.",
    "The problem addressed by this project is therefore to build an open, Bengaluru-inspired "
    "simulation environment for non-lane mixed traffic, to design a decentralised, "
    "self-learning signal controller that works well in it, and to compare that controller "
    "fairly with established baselines using measures that matter to Indian road users.",
)
heading("1.3 Objectives", 2)
para("The objectives of the project are listed below. They are grouped into three parts: "
     "the environment, the controller and the evaluation.")
bullets([
    "To build a SUMO sublane simulation of a four-junction arterial corridor with five "
    "Indian vehicle classes (two-wheeler, auto-rickshaw, car, bus and truck) in which "
    "smaller vehicles filter laterally without lane discipline.",
    "To check the simulated flows and signal timings against manual vehicle counts taken "
    "at two Bengaluru junctions and against publicly available signal timing data.",
    "To release the environment openly so that other groups can test their own controllers "
    "on Indian traffic.",
    "To measure the demand on each approach as a PCU-weighted queue rather than a count of "
    "vehicles.",
    "To train a PPO agent at every signalised junction of the corridor.",
    "To let neighbouring agents exchange short messages (PCU released, estimated arrival "
    "time and a priority flag) so that green waves can form along the arterial.",
    "To give ambulances a priority green corridor along their route.",
    "To define and measure a cross-street recovery time after an ambulance has passed.",
    "To enforce a safety shell of minimum green, maximum green, yellow and all-red "
    "intervals that the learning agent cannot override.",
    "To retrain the agents every night on the previous day's demand so that the controller "
    "keeps up with changing traffic.",
    "To compare the controller with fixed-time control, Max Pressure, MPLight and CoLight "
    "inside the same environment.",
    "To report average delay, ambulance travel time, cross-street recovery time and delay "
    "for each vehicle class.",
], numbered=True)
heading("1.4 Summary", 2)
text(
    "Signal control in Indian cities has to deal with traffic that is mixed and does not "
    "keep to lanes, while the learning controllers described in the literature assume the "
    "opposite. This chapter set out why that mismatch matters, stated the problem and "
    "listed twelve objectives covering the environment, the controller and the evaluation. "
    "Chapter 2 reviews the published work on which the project builds, and Chapter 3 "
    "describes the proposed approach, the system architecture, what has been completed so "
    "far and what remains for Phase II.",
)

# ================================================= CHAPTER 2
chapter(2, "Literature Survey")
heading("2.1 Introduction", 2)
text(
    "The survey covers four areas that the project draws on: classical adaptive signal "
    "control, reinforcement learning for single and multiple junctions, emergency vehicle "
    "priority and safety, and the modelling of Indian heterogeneous traffic. We restricted "
    "ourselves to papers published in peer-reviewed journals, together with the Indian "
    "Roads Congress guideline on capacity. Some well-known controllers, such as IntelliLight, "
    "PressLight, MPLight and CoLight, first appeared at conferences. Where we mention them, "
    "we rely on the description given in the journal survey by Wei et al. [11].",
)
heading("2.2 Literature Survey", 2)
heading("2.2.1 Classical and adaptive signal control", 3)
text(
    "Sims and Dobinson [2] described the philosophy behind SCATS, the Sydney Coordinated "
    "Adaptive Traffic System. SCATS uses stop-line detectors to estimate the degree of "
    "saturation on each approach and then adjusts cycle length, green splits and offsets "
    "for groups of junctions. It is organised as a hierarchy of local controllers and "
    "regional computers. The strength of the system is that it has been deployed at scale "
    "for many years. Its weakness, from our point of view, is that the adjustment rules are "
    "fixed by engineers and do not learn from experience.",
    "Mirchandani and Head [3] presented RHODES, a real-time traffic-adaptive system with a "
    "layered architecture. At the network level it estimates flows. At the junction level "
    "it predicts vehicle arrivals from upstream detectors and chooses phase durations with "
    "dynamic programming over a short horizon. RHODES showed that prediction, and not only "
    "measurement, can improve timing decisions, but it depends on reliable detector data "
    "and a hand-built traffic model.",
    "Varaiya [1] proposed Max Pressure control for a network of signalised junctions. At "
    "each junction the controller gives green to the phase with the largest pressure, "
    "which is the difference between the queues upstream and downstream of that phase. The "
    "paper proves that, when demand lies within the capacity of the network, this simple "
    "local rule keeps all queues bounded, and it needs no knowledge of demand. Because it "
    "is decentralised and has a proof behind it, Max Pressure has become one of the "
    "standard baselines for learning controllers, and it is one of ours.",
    "Zhao et al. [4] surveyed computational intelligence methods for urban signal control, "
    "including fuzzy logic, neural networks, evolutionary algorithms and early "
    "reinforcement learning. The survey noted that most methods were tested only in small "
    "simulated networks and pointed to learning methods as a promising direction.",
)
heading("2.2.2 Reinforcement learning for a single junction", 3)
text(
    "Abdulhai et al. [5] were among the first to apply Q-learning to signal control. Their "
    "agent controlled an isolated junction and learned from the queue lengths it observed. "
    "Under variable demand it did better than a pre-timed plan. The work was limited to a "
    "single junction and a small, hand-designed state space.",
    "The arrival of deep reinforcement learning, shown most clearly by Mnih et al. [7], who "
    "trained a deep Q-network to play Atari games at human level from raw pixels, made it "
    "possible to use richer state descriptions. Li et al. [8] used a stacked autoencoder to "
    "estimate action values for signal timing at a single junction and reported lower "
    "delay than a conventional RL controller. Liang et al. [9] treated the junction as an "
    "image-like grid of vehicle positions and speeds and trained a double dueling deep "
    "Q-network with prioritised experience replay in SUMO to adjust phase durations within "
    "a cycle.",
    "Kumar et al. [15] placed a fuzzy inference system alongside a deep RL agent so that "
    "the phase decision reflects traffic conditions described in linguistic terms, and they "
    "treated emergency vehicles as a separate case. Agarwal et al. [16] are closest to our "
    "setting. They studied Max Pressure and RL controllers under heterogeneous traffic "
    "conditions of the kind found in India and showed that vehicle composition changes how "
    "these controllers should be designed. Their experiments were carried out on a single "
    "junction and did not come with an openly released environment for multi-junction "
    "coordination.",
)
heading("2.2.3 Multi-agent and coordinated control", 3)
text(
    "El-Tantawy et al. [6] developed MARLIN-ATSC, in which each junction is an RL agent "
    "that takes the actions of its neighbours into account. It was applied to a large "
    "microsimulation model of downtown Toronto and reduced average delay compared with the "
    "existing signal plans. The work showed that decentralised agents can coordinate "
    "without a central computer, which is the design we follow.",
    "Chu et al. [10] proposed a multi-agent advantage actor-critic method for large-scale "
    "signal control. Each agent includes information about its neighbours' policies in its "
    "own state, and a spatial discount factor reduces the weight of distant junctions. It "
    "was evaluated on a synthetic grid and on a model of Monaco in SUMO. Wang et al. [12] "
    "proposed STMARL, which uses a graph neural network to capture the spatial relations "
    "between signals and a recurrent network to capture how traffic changes over time.",
    "Wei et al. [11] surveyed RL-based signal control models and the ways they are "
    "evaluated. Their survey describes PressLight, which uses the Max Pressure idea as a "
    "reward, MPLight, which shares parameters across junctions and scales to thousands of "
    "signals, and CoLight, which uses graph attention to decide how much each neighbour "
    "should influence a junction's decision. The survey also points out that different "
    "papers use different simulators, networks and demand files, which makes their "
    "results hard to compare. Haydari and Yilmaz [13] and Noaeen et al. [14] reached similar "
    "conclusions in their broader reviews: evaluation is almost always done in simulation, "
    "real deployments are rare, and the test networks come from a small number of "
    "countries. Zhu et al. [19] reviewed multi-agent RL with explicit communication and "
    "organised the design choices around what agents share, with whom and when. That "
    "framework guided the design of our short neighbour messages.",
)
heading("2.2.4 Emergency priority, safety and adaptation", 3)
text(
    "Nellore and Hancke [18] proposed a camera-based traffic management scheme that "
    "estimates congestion and clears the way for emergency vehicles. Su et al. [17] "
    "presented EMVLight, a multi-agent RL framework that routes an emergency vehicle and "
    "controls signals together. It reduced the emergency vehicle's travel time and also "
    "limited the harm to other traffic, measured as average travel time. It did not report "
    "how long the side streets took to return to normal once the emergency vehicle had "
    "gone, which is the quantity our recovery metric captures.",
    "García and Fernández [20] reviewed safe reinforcement learning and separated it into "
    "two families: methods that change the optimisation objective and methods that change "
    "or restrict the exploration process using outside knowledge. Our safety shell belongs "
    "to the second family. It is a fixed layer of rules that the agent's actions pass "
    "through before they reach the signal. Ke et al. [28] showed that transfer learning "
    "helps deep RL controllers, in their case for variable speed limits, adapt to new "
    "traffic conditions without training from scratch. This supports our plan to retrain "
    "each night starting from the previous day's policy.",
)
heading("2.2.5 Indian heterogeneous traffic and simulation", 3)
text(
    "Chandra and Kumar [21] studied how lane width affects capacity under mixed traffic in "
    "India and showed that PCU values are not constant but change with road width and "
    "traffic composition. Mondal et al. [26] estimated PCU values for urban arterials in "
    "Kolkata and reached a similar conclusion. IRC:106-1990 [29] gives the standard PCU "
    "values used in Indian practice, and these are the values we adopt.",
    "Arasan and Koshy [22] developed a simulation method for highly heterogeneous traffic in "
    "which each vehicle occupies a rectangle on the road surface instead of a lane. Mathew "
    "and Radhakrishnan [23] calibrated a microsimulation model for non-lane heterogeneous "
    "traffic at signalised junctions and showed that default parameters give poor results "
    "unless they are tuned to local data. Kanagaraj et al. [24] collected vehicle "
    "trajectories from an Indian urban road and described the flow characteristics of mixed "
    "traffic, and Asaithambi et al. [25] reviewed driving behaviour models for non-lane "
    "traffic and listed the open challenges. Krajzewicz et al. [27] described SUMO, the "
    "open-source microscopic simulator we use. Its sublane model divides each lane into "
    "narrow strips so that vehicles can move sideways and ride side by side, which is what "
    "non-lane traffic needs.",
)
table("Table 2.1: Summary of the reviewed literature", [
    ["Ref.", "Method", "Setting", "Limitation for Indian traffic"],
    ["[2]", "SCATS, rule-based adaptive", "Deployed network", "Fixed rules, does not learn"],
    ["[3]", "RHODES, prediction and dynamic programming", "Network, detectors",
     "Needs a hand-built traffic model"],
    ["[1]", "Max Pressure", "Network, theory", "Counts vehicles, not load"],
    ["[5]", "Q-learning", "Single junction", "Small state space, lane traffic"],
    ["[8], [9]", "Deep Q-learning", "Single junction", "Lane-based simulation"],
    ["[6]", "MARLIN-ATSC multi-agent RL", "Toronto network", "Lane traffic, no emergency case"],
    ["[10]", "Multi-agent actor-critic", "Grid and Monaco", "Lane traffic, vehicle counts"],
    ["[12]", "Graph and recurrent multi-agent RL", "Synthetic and real networks",
     "Lane traffic"],
    ["[11]", "Survey (PressLight, MPLight, CoLight)", "Benchmarks",
     "No Indian non-lane benchmark"],
    ["[15]", "Fuzzy inference with deep RL", "Single junction", "No coordination"],
    ["[16]", "Max Pressure and RL, heterogeneous traffic", "Single junction",
     "No corridor, no open environment"],
    ["[17]", "EMVLight, emergency routing and control", "Grid networks",
     "No cross-street recovery measure"],
    ["[22], [23]", "Non-lane heterogeneous simulation", "Indian roads",
     "No signal learning"],
], [0.8, 2.2, 1.5, 2.2], size=10)
text(
    "Table 2.2 sets the reviewed work against the four features that, taken together, "
    "no single study provides.",
)
table("Table 2.2: Research gap addressed by Saarathi", [
    ["Feature", "Existing work", "Saarathi"],
    ["Open environment for non-lane mixed traffic",
     "Benchmarks use lane-disciplined networks from outside India [11], [14]",
     "SUMO sublane corridor with five Indian classes, released openly"],
    ["Coordination on mixed traffic",
     "Coordination studied on lane traffic [6], [10], [12]; heterogeneous work is single "
     "junction [16]", "Neighbour messages in PCU, green waves on a four-junction corridor"],
    ["Cost of emergency priority",
     "Emergency travel time and average delay [17]",
     "Ambulance travel time plus cross-street recovery time"],
    ["Scores of known controllers on Indian traffic",
     "Not available", "Fixed-time, Max Pressure, MPLight and CoLight in the same environment"],
], [1.6, 2.3, 2.3], size=10, align0=False)
heading("2.3 Summary", 2)
text(
    "The literature shows a steady move from rule-based adaptive systems to learning agents "
    "and from single junctions to coordinated networks. Max Pressure gives a strong and "
    "simple baseline with a proof behind it, and multi-agent RL methods such as MARLIN-ATSC, "
    "MA2C, CoLight and STMARL show that decentralised agents can coordinate. Indian research "
    "on heterogeneous traffic, on the other hand, has concentrated on capacity, PCU and "
    "simulation, not on learning controllers. The two lines of work have hardly met. The "
    "gaps are an open environment for non-lane traffic, coordination measured in PCU, a "
    "measure of what emergency priority costs the cross streets, and a fair comparison of "
    "known controllers on Indian traffic. Saarathi is designed to fill these gaps.",
)

# ================================================= CHAPTER 3
chapter(3, "Methodology")
text(
    "This chapter explains the approach we have chosen and the reasons behind each "
    "choice, and then describes the architecture of the system, the flow of the proposed "
    "algorithm and the order in which the parts interact during one decision step.",
)
heading("3.1 Proposed Approach", 2)
heading("3.1.1 Choice of model", 3)
text(
    "Signal control fits naturally into the reinforcement learning framework. The "
    "controller observes the junction, chooses an action, and the traffic responds. No "
    "labelled data exists that says which phase was the correct one at a given second, so "
    "supervised learning is not an option. The quality of a decision shows up only later, "
    "as queues that grow or shrink, which is exactly the delayed reward that RL is designed "
    "to handle [13].",
    "Among RL algorithms we chose Proximal Policy Optimisation (PPO), an actor-critic "
    "method that limits how far the policy can change in one update by clipping the "
    "probability ratio between the new and old policies. We preferred it to deep "
    "Q-learning [7]–[9] for three reasons. First, its updates are stable, which matters "
    "when several agents learn at once and each one's environment keeps shifting as its "
    "neighbours change their behaviour. Second, it works directly with a stochastic "
    "policy, so the safety shell can mask out forbidden actions without breaking the "
    "learning rule. Third, it needs little tuning, and mature open implementations exist; "
    "we use Stable-Baselines3. We use one agent per junction with shared network weights, "
    "which keeps training cost low and lets experience at one junction help the others, an "
    "idea also used by MPLight as described in [11].",
)
heading("3.1.2 The simulation environment", 3)
text(
    "The environment is a corridor of four signalised junctions, J1 to J4, placed 300 m "
    "apart on an east-west arterial 1.5 km long. The arterial has two lanes in each "
    "direction with a speed limit of 13.9 m/s (50 km/h). Each junction has a north and a "
    "south side street 200 m long, with one lane and a limit of 11.1 m/s (40 km/h). The "
    "simulation step is 1.0 s and the sublane resolution is 0.4 m, so a 3.2 m lane is "
    "divided into eight strips and a two-wheeler can pass between two cars.",
    "Table 3.1 lists the five vehicle classes. Two-wheelers and auto-rickshaws may take any "
    "lateral position and keep only a small side gap from other vehicles, while cars, buses "
    "and trucks keep to the centre of their lane. The vehicle mix follows a Bengaluru-like "
    "split of 45 per cent two-wheelers, 22 per cent cars, 15 per cent auto-rickshaws, 8 per "
    "cent buses and 10 per cent trucks. Demand follows a 24-hour profile with a morning "
    "peak from 9 to 11 a.m. and an evening peak from 5 to 8 p.m.",
)
table("Table 3.1: Vehicle classes used in the simulation", [
    ["Class", "Length (m)", "Width (m)", "Max speed (m/s)", "Lateral behaviour", "PCU",
     "Share (%)"],
    ["Two-wheeler", "2.0", "0.75", "16.7", "Free, side gap 0.25 m", "0.5", "45"],
    ["Auto-rickshaw", "3.0", "1.4", "13.9", "Free, side gap 0.35 m", "1.2", "15"],
    ["Car", "4.4", "1.8", "19.4", "Lane centre", "1.0", "22"],
    ["Bus", "12.0", "2.5", "13.9", "Lane centre", "3.0", "8"],
    ["Truck", "9.5", "2.4", "13.9", "Lane centre", "3.0", "10"],
], [1.3, 0.8, 0.8, 0.9, 1.7, 0.6, 0.7], size=10)
heading("3.1.3 State, action and reward", 3)
text(
    "The key choice in the state is how demand is measured. For each approach a of a "
    "junction, the agent sees the PCU-weighted queue, which is the sum of the PCU values of "
    "all vehicles on that approach that are moving slower than 0.3 m/s:",
)
eq("Q_{a}(t) = Σ PCU(v),   for all v ∈ H_{a}(t)", "3.1")
text(
    "where H_{a}(t) is the set of halted vehicles on approach a at time t and PCU(v) is "
    "taken from Table 3.1. Queues are divided by 40 so that the inputs lie roughly between "
    "0 and 1. The full observation of a junction is then",
)
eq("s_{t} = [ Q_{1}/40, …, Q_{4}/40, p_{t}, g_{t}, sin(2πh/24), cos(2πh/24), d ]", "3.2")
text(
    "in which p_{t} is a one-hot code of the current phase, g_{t} is the time spent in the "
    "current green, h is the hour of the day and d marks weekdays. The time terms let the "
    "agent tell the morning peak from the midday lull. Messages from neighbouring "
    "junctions, described in Section 3.1.5, are appended to this vector.",
    "Every 5 s the agent chooses between two actions: keep the current phase or move to the "
    "next one. A small action space was chosen on purpose. It keeps learning fast, and it "
    "makes the safety shell easy to reason about. The reward at step t is",
)
eq("r_{t} = − Σ_{a} Q_{a}(t) / 100 − 0.5 · k_{t}", "3.3")
text(
    "where k_{t} is 1 if the agent asked to switch phase and 0 otherwise. The first term "
    "rewards the agent for keeping the total PCU queue short. The second is a small "
    "penalty for switching, since each switch wastes 5 s of yellow and all-red time. "
    "Because the queue is in PCU, a bus held at a red light costs the agent six times as "
    "much as a two-wheeler, which is roughly the difference in road space and "
    "passenger load between them.",
)
heading("3.1.4 Safety shell", 3)
text(
    "A learning agent should never be allowed to produce an unsafe signal sequence, no "
    "matter what it has learned. Following the idea of restricting exploration using "
    "outside knowledge [20], every action passes through a fixed rule layer before it "
    "reaches the signal. The rules are listed in Table 3.2. If the agent asks to switch "
    "before the minimum green is over, the request is ignored. If a phase reaches its "
    "maximum green, the switch is forced. Every change of phase goes through yellow and "
    "all-red. The agent learns inside these limits and can never leave them.",
)
table("Table 3.2: Signal timing rules enforced by the safety shell", [
    ["Rule", "Value", "Purpose"],
    ["Minimum green", "10 s", "Pedestrians can cross and the queue can start moving"],
    ["Maximum green", "60 s", "No approach is starved"],
    ["Yellow", "3 s", "Warning before the change"],
    ["All-red", "2 s", "Clears vehicles still inside the junction"],
    ["Decision interval", "5 s", "Limits how often the agent can act"],
], [1.5, 0.9, 3.4], size=10)
heading("3.1.5 Neighbour messages and green waves", 3)
text(
    "A junction that acts only on its own queues will often release a platoon just as the "
    "next junction turns red. To avoid this, each agent sends a short message to its "
    "upstream and downstream neighbours at every decision step. The message has three "
    "fields: the PCU it has just released towards that neighbour, the estimated time for "
    "that platoon to arrive, and a priority flag that is set when an ambulance is on the "
    "way. The arrival time is estimated from the link length and the current mean speed on "
    "the link:",
)
eq("ETA_{ij} = L_{ij} / v_{ij}", "3.4")
text(
    "where L_{ij} is the distance between junctions i and j (300 m here) and v_{ij} is the "
    "current mean speed on that link. The receiving agent adds these values to its observation. "
    "Over training it can learn to hold its green a little longer when a large platoon is "
    "due, which is how a green wave forms without any central plan. Keeping the message to "
    "three numbers makes it cheap to send and easy to interpret, in line with the design "
    "choices discussed by Zhu et al. [19].",
)
heading("3.1.6 Ambulance priority and cross-street recovery", 3)
text(
    "When an ambulance enters the corridor, the junction it is approaching raises the "
    "priority flag, and the flag is passed along the route in the neighbour messages. Each "
    "junction on the route then gives green to the ambulance's approach as soon as the "
    "safety shell allows it, so the minimum green, yellow and all-red rules still hold. "
    "Once the ambulance has cleared the junction, normal control resumes.",
    "Priority has a cost, and we want to measure it. We define the cross-street recovery "
    "time of junction j as the time from the moment the ambulance clears the junction until "
    "the PCU queue on its side streets falls back to within 10 per cent of the level "
    "expected without an ambulance:",
)
eq("T_{rec,j} = min{ τ ≥ 0 : Q^{side}_{j}(t_{c} + τ) ≤ 1.1 · Q^{ref}_{j} }", "3.5")
text(
    "where t_{c} is the clearing time and Q^{ref}_{j} is the side-street queue at the same "
    "time of day in an identical run without the ambulance. A controller that clears the "
    "ambulance quickly but leaves the side streets jammed for several minutes will show a "
    "large recovery time, and this makes the trade-off visible.",
)
heading("3.1.7 Nightly retraining", 3)
text(
    "Traffic in a growing city does not stay the same for long. New offices, a closed road "
    "or a school reopening can change the demand pattern within a few weeks. The controller "
    "therefore continues training each night. The day's detector data are turned into a "
    "demand file, the simulation is run with that demand, and the policy is updated "
    "starting from the previous day's weights, which is a simple form of the transfer "
    "strategy that Ke et al. [28] found effective. The new policy is used the next day only "
    "if it does at least as well as the old one on a held-out day of traffic. Table 3.3 "
    "lists the training settings.",
)
table("Table 3.3: PPO training settings", [
    ["Parameter", "Value"],
    ["Library", "Stable-Baselines3 (PPO)"],
    ["Steps collected per update", "512"],
    ["Mini-batch size", "128"],
    ["Learning rate", "0.0003"],
    ["Discount factor γ", "0.99"],
    ["Decision interval", "5 s of simulated time"],
    ["Policy", "One network shared by all four junctions"],
], [2.8, 2.8], size=10)
heading("3.1.8 Implementation status and preliminary results", 3)
text(
    "The corridor described in Section 3.1.2 has been built and runs. Figure 3.1 shows its "
    "layout: four signalised junctions 300 m apart on a 1.5 km arterial, each with a north "
    "and a south side street, and neighbour messages travelling in both directions along "
    "the arterial. The network, the sublane settings, the five vehicle types, the demand "
    "generator and the 24-hour profile are all in place, and the environment exposes the "
    "usual reset and step interface so that a controller can be attached to it.",
)
figure("corridor.png", "Figure 3.1: Layout of the four-junction corridor and the neighbour "
       "messages", width=TEXTW - 0.4)
text(
    "One hour of morning-peak traffic was run to check that the environment behaves as "
    "intended. Of the 4162 vehicles that completed a trip, the total load came to 4873 PCU, "
    "so the corridor carried about seventeen per cent more road space than a plain vehicle "
    "count would suggest. The split matters more than the total. Two-wheelers were 44.7 per "
    "cent of the vehicles but only 19.1 per cent of the PCU, while buses and trucks together "
    "were 18.2 per cent of the vehicles and 46.6 per cent of the PCU. A controller that "
    "counts vehicles therefore sees a corridor dominated by two-wheelers, and a controller "
    "that counts PCU sees one dominated by heavy vehicles. That is the difference Section "
    "3.1.3 depends on, and it is present in the simulation before any control decision is "
    "taken. The sublane model is active throughout, with a lateral resolution of 0.4 m and "
    "free lateral alignment for the two small classes, so filtering is represented in the "
    "model; measuring the lateral displacement each class actually takes up is part of the "
    "Phase II runs.",
)
text(
    "The PCU sensing module of (3.1), the observation vector of (3.2), the reward of (3.3) "
    "and the safety shell of Table 3.2 have been implemented and tested against the "
    "simulator. The shell was checked by feeding it deliberately illegal requests, such as "
    "a switch two seconds after a phase change, and confirming that the signal sequence it "
    "produced still respected every limit. The definitions of the neighbour message, of the "
    "ambulance priority flag and of the cross-street recovery time in (3.5) have been "
    "fixed, and the logging needed to compute them is in place.",
)
text(
    "Two baselines have been implemented and run on one hour of morning-peak demand. "
    "Fixed-time control gave an average delay of 66.5 s per vehicle and an average travel "
    "time of 138.9 s over 4162 vehicles. Max Pressure, still counting vehicles rather than "
    "PCU, gave 46.4 s and 118.9 s over 4179 vehicles. Figure 3.2 shows the two sets of "
    "figures side by side.",
)
figure("baseline.png", "Figure 3.2: Average delay and travel time under fixed-time control "
       "and Max Pressure in the morning peak", width=5.2)
text(
    "Even a simple adaptive rule therefore cuts average delay by about thirty per cent "
    "relative to a fixed plan on this corridor. The result is useful in two ways. It shows "
    "that the environment reacts to control decisions the way a real junction would, and it "
    "sets the target that the learning controller has to beat before it is worth using.",
)
heading("3.1.9 Remaining work and expected outcome", 3)
text(
    "The work that remains turns the environment and the definitions above into a trained "
    "and measured controller. A PPO agent will be trained at each of the four junctions "
    "with the settings of Table 3.3 and a single shared policy network, starting from one "
    "junction with the other three under fixed-time control so that the learning curve can "
    "be checked before all four agents are allowed to learn together. The neighbour "
    "messages will then be switched on and the agents retrained, and the green wave will be "
    "looked for in the resulting phase patterns and not only in the delay numbers. The "
    "ambulance module will be added and the cross-street recovery time of (3.5) measured, "
    "each ambulance run being paired with an identical run without the ambulance so that "
    "the reference side-street queue is available.",
)
text(
    "Manual counts will be taken at two Bengaluru junctions during a morning peak and an "
    "off-peak hour, recording vehicle class and, where possible, queue length, and "
    "published signal timings will be obtained from the open city data portal. The "
    "simulated flows and the modal split will be compared with those counts and the demand "
    "generator adjusted until the difference is acceptable, which is what allows the "
    "environment to be called Indian rather than merely heterogeneous. MPLight and CoLight "
    "will then be re-implemented from the descriptions given in the journal survey [11] and "
    "their public implementations, and every controller will be run on the same demand "
    "files with the same random seeds. Finally the retraining loop of Section 3.1.7 will be "
    "automated and the environment, the network files, the demand generator, the baseline "
    "implementations and the evaluation scripts will be packaged and released.",
)
text(
    "At the end of the project the following outcomes are expected.",
)
bullets([
    "An open simulation environment for non-lane mixed traffic on a four-junction corridor, "
    "with five Indian vehicle classes, PCU-weighted demand and a documented interface, "
    "calibrated against counts taken at two Bengaluru junctions.",
    "A decentralised PPO controller that senses demand in PCU, exchanges short messages "
    "with its neighbours, forms green waves along the arterial and operates inside a fixed "
    "safety shell.",
    "An ambulance priority mechanism reported together with the cross-street recovery time, "
    "so that the cost of priority to the side streets is measured and not hidden.",
    "A retraining pipeline that keeps the policy in step with changing demand and refuses "
    "to deploy a policy that has become worse.",
    "A like-for-like comparison of fixed-time control, Max Pressure, MPLight, CoLight and "
    "Saarathi in one environment, reporting average delay, ambulance travel time, "
    "cross-street recovery time and per-class delay.",
    "A journal paper describing the environment, the controller and the comparison, and a "
    "public code release that allows the results to be reproduced.",
])
text(
    "Success will be judged on three things: whether the controller beats Max Pressure on "
    "average delay in the same environment, whether it shortens ambulance travel time "
    "without leaving the side streets jammed for long, and whether another group can take "
    "the released environment and reproduce the numbers reported here.",
)

heading("3.2 System Architecture", 2)
heading("3.2.1 Components of the architecture", 3)
text(
    "Figure 3.3 shows the architecture of Saarathi. It is organised in three layers, one "
    "for each part of the project: the environment in which the traffic moves, the "
    "controller that decides the signal timings, and the evaluation machinery that measures "
    "how well the controller does.",
)
figure("arch.png", "Figure 3.3: System architecture of Saarathi")
heading("Environment layer", 4)
text(
    "SUMO runs the four-junction corridor with the sublane model switched on. A demand "
    "generator produces vehicles according to the modal split of Table 3.1 and the 24-hour "
    "profile, and a calibration step compares the resulting flows with counts taken in the "
    "field. The whole layer is wrapped as a Gymnasium-style environment so that any "
    "controller, learned or rule-based, can be plugged into it through the same interface. "
    "This is the part of the work we intend to release openly.",
)
heading("Controller layer", 4)
text(
    "At each junction a sensing module converts the vehicles on every approach into the "
    "PCU-weighted queues of (3.1). The PPO agent reads those queues together with the time "
    "features and the messages received from its neighbours, and proposes an action. The "
    "proposed action is passed to the safety shell, which checks it against the rules of "
    "Table 3.2 before it is written to the signal through TraCI, the control interface of "
    "SUMO. An ambulance module can raise the priority flag on a route, and a nightly "
    "retraining job updates the shared policy from the previous day's demand.",
)
heading("Evaluation layer", 4)
text(
    "The same environment also runs the baseline controllers, so that every controller sees "
    "identical demand files and identical random seeds. A metrics module logs average "
    "delay, travel time, ambulance travel time, cross-street recovery time and delay for "
    "each vehicle class, and writes them to a single results file that the comparison "
    "scripts read.",
)
heading("3.2.2 Flow of the proposed algorithm", 3)
text(
    "Figure 3.4 shows the flow that the controller follows at every decision step. The "
    "important point is the order of the blocks. Sensing comes first, then the neighbour "
    "messages are folded into the observation, then the policy proposes an action, and only "
    "after the ambulance check and the safety shell does anything reach the signal. Because "
    "the shell is the last block before the signal, no policy, however badly trained, can "
    "produce a timing sequence that breaks the minimum green, the maximum green or the "
    "clearance intervals.",
)
figure("flow.png", "Figure 3.4: Flowchart of the proposed algorithm", width=4.4)
heading("3.2.3 Decision flow at a junction", 3)
text(
    "Figure 3.5 shows the same decision step as an exchange of messages between the parts "
    "of the system over one interval of 5 s at a single junction. The steps are as follows.",
)
figure("seq.png", "Figure 3.5: Sequence diagram of one decision step")
bullets([
    "SUMO advances the simulation by one step and TraCI reads the position, speed and class "
    "of every vehicle near the junction.",
    "The sensing module picks out the halted vehicles on each approach and adds up their "
    "PCU values to form the queues in (3.1).",
    "The latest messages from the upstream and downstream junctions are added to the "
    "observation, giving the state in (3.2).",
    "The PPO agent computes a probability for each action and samples one.",
    "If an ambulance is approaching, the priority flag overrides the agent's choice and the "
    "ambulance's approach is given green as soon as the shell allows it.",
    "The safety shell checks the action. A switch requested before minimum green is "
    "refused, a phase at maximum green is ended, and every switch goes through yellow and "
    "all-red.",
    "The approved phase is written to the signal through TraCI.",
    "The junction sends its message (PCU released, arrival time, priority flag) to its "
    "neighbours.",
    "The reward (3.3) is computed and the transition is stored for the next PPO update. "
    "During evaluation, the metrics module records delay and, after an ambulance has "
    "passed, the cross-street recovery time.",
], numbered=True)
heading("3.2.4 Advantages of the proposed methodology", 3)
text(
    "Taken together, the design decisions described in this chapter give the proposed "
    "system the following properties.",
)
bullets([
    "**Demand measured in road space.** Queues are counted in PCU, so a bus or a truck "
    "weighs what it actually costs the junction instead of counting as one vehicle.",
    "**Built for non-lane traffic.** The environment uses the sublane model, so filtering "
    "by two-wheelers and auto-rickshaws is represented rather than assumed away.",
    "**Decentralised.** Every junction decides for itself and exchanges three numbers with "
    "its neighbours, so there is no central computer to fail and the design does not become "
    "harder as junctions are added.",
    "**Safe by construction.** Timing limits live outside the learned policy, which makes "
    "the controller acceptable to a traffic engineer who does not want to trust a neural "
    "network with clearance times.",
    "**Priority with a measured cost.** Ambulance priority is reported together with the "
    "cross-street recovery time, so the price paid by the side streets is visible.",
    "**Able to follow a changing city.** Nightly retraining starts from the previous day's "
    "policy, and a new policy is used only if it does at least as well on a held-out day.",
    "**Comparable.** Every controller is run in the same environment with the same demand "
    "and the same seeds, which is exactly what the surveys say the field is missing.",
])

heading("3.2.5 Software and Computing Specifications", 3)
text(
    "The project is built and evaluated entirely in simulation, so no purpose-built hardware "
    "is involved. The specifications below record the machine the corridor runs on and the "
    "software the implementation depends on, so that the results reported in Section 3.1.8 "
    "can be reproduced. Training uses the CPU; the policy network is small enough that a "
    "GPU gives no useful advantage at this scale.",
)
table("Table 3.4: Computing platform used for development and experiments", [
    ["Item", "Specification"],
    ["Processor", "Apple M5 Pro"],
    ["Memory", "48 GB unified memory"],
    ["Operating system", "macOS 26.6.2"],
    ["Accelerator", "None used; PPO on this network size trains on the CPU"],
], [1.7, 4.3])
table("Table 3.5: Software stack", [
    ["Component", "Version and role"],
    ["Language", "Python 3.14.5"],
    ["Simulator", "SUMO 1.27.1, sublane model, driven through the TraCI interface"],
    ["Learning library", "Stable-Baselines3 2.9.0 (PPO) on PyTorch 2.14.0"],
    ["Environment interface", "Gymnasium 1.3.0"],
    ["Numerical and plotting", "NumPy 2.5.1, Matplotlib 3.11.2"],
    ["Version control", "Git; the environment and the evaluation scripts are to be "
     "released publicly"],
], [1.7, 4.3])

# ================================================= REFERENCES
sec = doc.add_section(WD_SECTION.NEW_PAGE)
a4(sec)
set_pgnum(sec)
para("REFERENCES", 16, True, C, after=12, spacing=1.5)
REFS = [
    ("P. Varaiya, \"Max pressure control of a network of signalized intersections,\" ",
     "Transp. Res. Part C, Emerg. Technol.", ", vol. 36, pp. 177–195, Nov. 2013."),
    ("A. G. Sims and K. W. Dobinson, \"The Sydney coordinated adaptive traffic (SCAT) system "
     "philosophy and benefits,\" ", "IEEE Trans. Veh. Technol.",
     ", vol. 29, no. 2, pp. 130–137, May 1980."),
    ("P. Mirchandani and L. Head, \"A real-time traffic signal control system: architecture, "
     "algorithms, and analysis,\" ", "Transp. Res. Part C, Emerg. Technol.",
     ", vol. 9, no. 6, pp. 415–432, Dec. 2001."),
    ("D. Zhao, Y. Dai, and Z. Zhang, \"Computational intelligence in urban traffic signal "
     "control: A survey,\" ", "IEEE Trans. Syst., Man, Cybern. C, Appl. Rev.",
     ", vol. 42, no. 4, pp. 485–494, Jul. 2012."),
    ("B. Abdulhai, R. Pringle, and G. J. Karakoulas, \"Reinforcement learning for true "
     "adaptive traffic signal control,\" ", "J. Transp. Eng.",
     ", vol. 129, no. 3, pp. 278–285, May 2003."),
    ("S. El-Tantawy, B. Abdulhai, and H. Abdelgawad, \"Multiagent reinforcement learning "
     "for integrated network of adaptive traffic signal controllers (MARLIN-ATSC): "
     "Methodology and large-scale application on downtown Toronto,\" ",
     "IEEE Trans. Intell. Transp. Syst.", ", vol. 14, no. 3, pp. 1140–1150, Sep. 2013."),
    ("V. Mnih et al., \"Human-level control through deep reinforcement learning,\" ",
     "Nature", ", vol. 518, no. 7540, pp. 529–533, Feb. 2015."),
    ("L. Li, Y. Lv, and F.-Y. Wang, \"Traffic signal timing via deep reinforcement "
     "learning,\" ", "IEEE/CAA J. Autom. Sinica", ", vol. 3, no. 3, pp. 247–254, Jul. 2016."),
    ("X. Liang, X. Du, G. Wang, and Z. Han, \"A deep reinforcement learning network for "
     "traffic light cycle control,\" ", "IEEE Trans. Veh. Technol.",
     ", vol. 68, no. 2, pp. 1243–1253, Feb. 2019."),
    ("T. Chu, J. Wang, L. Codecà, and Z. Li, \"Multi-agent deep reinforcement learning for "
     "large-scale traffic signal control,\" ", "IEEE Trans. Intell. Transp. Syst.",
     ", vol. 21, no. 3, pp. 1086–1095, Mar. 2020."),
    ("H. Wei, G. Zheng, V. Gayah, and Z. Li, \"Recent advances in reinforcement learning for "
     "traffic signal control: A survey of models and evaluation,\" ",
     "ACM SIGKDD Explor. Newsl.", ", vol. 22, no. 2, pp. 12–18, Jan. 2021."),
    ("Y. Wang, T. Xu, X. Niu, C. Tan, E. Chen, and H. Xiong, \"STMARL: A spatio-temporal "
     "multi-agent reinforcement learning approach for cooperative traffic light control,\" ",
     "IEEE Trans. Mobile Comput.", ", vol. 21, no. 6, pp. 2228–2242, Jun. 2022."),
    ("A. Haydari and Y. Yilmaz, \"Deep reinforcement learning for intelligent transportation "
     "systems: A survey,\" ", "IEEE Trans. Intell. Transp. Syst.",
     ", vol. 23, no. 1, pp. 11–32, Jan. 2022."),
    ("M. Noaeen, A. Naik, L. Goodman, J. Crebo, T. Abrar, Z. S. H. Abad, A. L. C. Bazzan, "
     "and B. Far, \"Reinforcement learning in urban network traffic signal control: A "
     "systematic literature review,\" ", "Expert Syst. Appl.",
     ", vol. 199, Art. no. 116830, Aug. 2022."),
    ("N. Kumar, S. S. Rahman, and N. Dhakad, \"Fuzzy inference enabled deep reinforcement "
     "learning-based traffic light control for intelligent transportation system,\" ",
     "IEEE Trans. Intell. Transp. Syst.", ", vol. 22, no. 8, pp. 4919–4928, Aug. 2021."),
    ("A. Agarwal, D. Sahu, R. Mohata, K. Jeengar, A. Nautiyal, and D. K. Saxena, \"Dynamic "
     "traffic signal control for heterogeneous traffic conditions using Max Pressure and "
     "Reinforcement Learning,\" ", "Expert Syst. Appl.",
     ", vol. 254, Art. no. 124416, Nov. 2024."),
    ("H. Su, Y. D. Zhong, J. Y. J. Chow, B. Dey, and L. Jin, \"EMVLight: A multi-agent "
     "reinforcement learning framework for an emergency vehicle decentralized routing and "
     "traffic signal control system,\" ", "Transp. Res. Part C, Emerg. Technol.",
     ", vol. 146, Art. no. 103955, Jan. 2023."),
    ("K. Nellore and G. P. Hancke, \"Traffic management for emergency vehicle priority based "
     "on visual sensing,\" ", "Sensors", ", vol. 16, no. 11, Art. no. 1892, Nov. 2016."),
    ("C. Zhu, M. Dastani, and S. Wang, \"A survey of multi-agent deep reinforcement learning "
     "with communication,\" ", "Auton. Agents Multi-Agent Syst.",
     ", vol. 38, no. 1, Art. no. 4, Jan. 2024."),
    ("J. García and F. Fernández, \"A comprehensive survey on safe reinforcement "
     "learning,\" ", "J. Mach. Learn. Res.", ", vol. 16, no. 42, pp. 1437–1480, 2015."),
    ("S. Chandra and U. Kumar, \"Effect of lane width on capacity under mixed traffic "
     "conditions in India,\" ", "J. Transp. Eng.", ", vol. 129, no. 2, pp. 155–160, Mar. 2003."),
    ("V. T. Arasan and R. Z. Koshy, \"Methodology for modeling highly heterogeneous traffic "
     "flow,\" ", "J. Transp. Eng.", ", vol. 131, no. 7, pp. 544–551, Jul. 2005."),
    ("T. V. Mathew and P. Radhakrishnan, \"Calibration of microsimulation models for "
     "nonlane-based heterogeneous traffic at signalized intersections,\" ",
     "J. Urban Plann. Dev.", ", vol. 136, no. 1, pp. 59–66, Mar. 2010."),
    ("V. Kanagaraj, G. Asaithambi, T. Toledo, and T.-C. Lee, \"Trajectory data and flow "
     "characteristics of mixed traffic,\" ", "Transp. Res. Rec.",
     ", vol. 2491, no. 1, pp. 1–11, Jan. 2015."),
    ("G. Asaithambi, V. Kanagaraj, and T. Toledo, \"Driving behaviors: Models and challenges "
     "for non-lane based mixed traffic,\" ", "Transp. Develop. Econ.",
     ", vol. 2, no. 2, Art. no. 19, Aug. 2016."),
    ("S. Mondal, S. Chakraborty, S. K. Roy, and A. Gupta, \"Estimation of passenger car unit "
     "for heterogeneous traffic stream of urban arterials: Case study of Kolkata,\" ",
     "Transp. Lett.", ", vol. 15, no. 10, pp. 1276–1288, Nov. 2023."),
    ("D. Krajzewicz, J. Erdmann, M. Behrisch, and L. Bieker, \"Recent development and "
     "applications of SUMO – Simulation of Urban MObility,\" ",
     "Int. J. Adv. Syst. Meas.", ", vol. 5, no. 3&4, pp. 128–138, Dec. 2012."),
    ("Z. Ke, Z. Li, Z. Cao, and P. Liu, \"Enhancing transferability of deep reinforcement "
     "learning-based variable speed limit control using transfer learning,\" ",
     "IEEE Trans. Intell. Transp. Syst.", ", vol. 22, no. 7, pp. 4684–4695, Jul. 2021."),
    ("Indian Roads Congress, ", "Guidelines for Capacity of Urban Roads in Plain Areas",
     ", IRC:106-1990. New Delhi, India: IRC, 1990."),
]
for k, (a, jn, rest) in enumerate(REFS, 1):
    p = para(align=J, after=6, spacing=1.15)
    p.paragraph_format.left_indent = Inches(0.45)
    p.paragraph_format.first_line_indent = Inches(-0.45)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(0.45))
    run(p, f"[{k}]\t" + a); run(p, jn, italic=True); run(p, rest)

# ================================================= TOC (page ii, after Acknowledgement)
TOC = [
    ("CHAPTER 1  INTRODUCTION", 0),
    ("1.1 Motivation", 1), ("1.2 Problem Statement", 1), ("1.3 Objectives", 1),
    ("1.4 Summary", 1),
    ("CHAPTER 2  LITERATURE SURVEY", 0),
    ("2.1 Introduction", 1), ("2.2 Literature Survey", 1),
    ("2.2.1 Classical and adaptive signal control", 2),
    ("2.2.2 Reinforcement learning for a single junction", 2),
    ("2.2.3 Multi-agent and coordinated control", 2),
    ("2.2.4 Emergency priority, safety and adaptation", 2),
    ("2.2.5 Indian heterogeneous traffic and simulation", 2),
    ("2.3 Summary", 1),
    ("CHAPTER 3  METHODOLOGY", 0),
    ("3.1 Proposed Approach", 1),
    ("3.1.1 Choice of model", 2), ("3.1.2 The simulation environment", 2),
    ("3.1.3 State, action and reward", 2), ("3.1.4 Safety shell", 2),
    ("3.1.5 Neighbour messages and green waves", 2),
    ("3.1.6 Ambulance priority and cross-street recovery", 2),
    ("3.1.7 Nightly retraining", 2),
    ("3.1.8 Implementation status and preliminary results", 2),
    ("3.1.9 Remaining work and expected outcome", 2),
    ("3.2 System Architecture", 1),
    ("3.2.1 Components of the architecture", 2),
    ("3.2.2 Flow of the proposed algorithm", 2),
    ("3.2.3 Decision flow at a junction", 2),
    ("3.2.4 Advantages of the proposed methodology", 2),
    ("3.2.5 Software and Computing Specifications", 2),
    ("REFERENCES", 0),
]
# save the body document before the front matter is finished off
doc.core_properties.title = TITLE
doc.core_properties.author = ", ".join(n for n, _ in TEAM)
doc.save(OUT_BODY)

doc, TEXTW = front, 5.77            # back to the college template document

FRONT = [("Acknowledgement", "i"), ("Abstract", "ii"), ("Table of Contents", "iii"),
         ("List of Figures", "iv"), ("List of Tables", "v")]
TOC = [(n, 0) for n, _ in FRONT] + TOC

# ---- Table of Contents (template's "List of Tables" section is reused for it)
retext(P(86), "TABLE OF CONTENTS")
for idx in (87, 88):
    body[idx].getparent().remove(body[idx])
new = []
hp = para(align=L, after=6, spacing=1.0)
hp.paragraph_format.tab_stops.add_tab_stop(Inches(TEXTW), WD_TAB_ALIGNMENT.RIGHT)
run(hp, "Content", 14, bold=True); run(hp, "\t"); run(hp, "Page No.", 14, bold=True)
new.append(hp._p)
for name, lvl in TOC:
    tp = para(align=L, after=0, spacing=1.0)
    tp.paragraph_format.left_indent = Inches(0.22 * lvl)
    tp.paragraph_format.tab_stops.add_tab_stop(
        Inches(TEXTW), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    run(tp, name, 12, bold=(lvl == 0))
    run(tp, "\t" + str(PAGES.get("toc:" + name, dict(FRONT).get(name, ""))), 12,
        bold=(lvl == 0))
    new.append(tp._p)
for el in new:
    move_before(el, body[89])

# ---- List of Figures and List of Tables, one page each
retext(P(90), "List of Figures")


def list_table(first, items):
    t = doc.add_table(rows=len(items) + 1, cols=3)
    brd = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + side)
        for k, v in (("val", "single"), ("sz", "4"), ("space", "0"), ("color", "000000")):
            e.set(qn("w:" + k), v)
        brd.append(e)
    t._tbl.tblPr.append(brd)
    t.alignment = 1
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(lay)
    widths = [0.9, 3.87, 1.0]
    for j, w in enumerate(widths):
        t.columns[j].width = Inches(w)
    rows = [(first, "Title", "Page No.")]
    for cap in items:
        head, rest = cap.split(" ", 2)[1].rstrip(":"), cap.split(" ", 2)[2]
        rows.append((head, rest, str(PAGES.get(cap, ""))))
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.width = Inches(widths[j])
            pp = c.paragraphs[0]
            pp.text = ""
            pp.paragraph_format.line_spacing = 1.0
            pp.paragraph_format.space_after = Pt(2)
            pp.alignment = L if (i and j == 1) else C
            run(pp, v, 12, bold=(i == 0))
    return t


list_table("Fig. No.", FIGS)
brk = para(align=L, after=0, spacing=1.0)
run(brk, "").add_break(WD_BREAK.PAGE)
para("List of Tables", 16, True, C, after=12, spacing=1.0)
list_table("Table No.", TABS)

doc.core_properties.title = TITLE
doc.core_properties.author = ", ".join(n for n, _ in TEAM)
doc.save(OUT)
json.dump({"caps": FIGS + TABS,
           "heads": [t for t, l in TOC if l]}, open(HERE / "captions.json", "w"))
print("saved", OUT, "and", OUT_BODY, len(FIGS), "figs", len(TABS), "tables")
