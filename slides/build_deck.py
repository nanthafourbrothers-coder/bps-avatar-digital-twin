from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

REPO = "github.com/nanthafourbrothers-coder/bps-avatar-digital-twin"
NAVY, TEAL, ORANGE = RGBColor(0x12,0x35,0x5b), RGBColor(0x1b,0x7f,0x8c), RGBColor(0xd9,0x82,0x2b)
INK, GREY, LIGHT, WHITE = RGBColor(0x1c,0x27,0x33), RGBColor(0x5d,0x6d,0x7e), RGBColor(0xee,0xf3,0xf8), RGBColor(0xfa,0xfb,0xfc)
FIG = "../figures/"
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
blank = prs.slide_layouts[6]
FONT = "Calibri"

def bg(s, color):
    f = s.background.fill; f.solid(); f.fore_color.rgb = color

def text(s, x, y, w, h, t, size=20, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor; tf.margin_left = tf.margin_right = Inches(0.05)
    lines = t if isinstance(t, list) else [t]
    for i, l in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = l; r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
        r.font.color.rgb = color; r.font.name = FONT; p.alignment = align; p.space_after = Pt(6)
    return tb

def rect(s, x, y, w, h, fill, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    r = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    r.fill.solid(); r.fill.fore_color.rgb = fill
    if line: r.line.color.rgb = line; r.line.width = Pt(1.2)
    else: r.line.fill.background()
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE: r.adjustments[0] = 0.06
    r.shadow.inherit = False
    return r

def footer(s, n, dark=False):
    c = RGBColor(0xb8,0xc7,0xd6) if dark else GREY
    text(s, 0.6, 6.95, 9, 0.35, "AVATAR-Twin  |  Nanthakumar R, New Way Concepts Research", 12, color=c)
    text(s, 11.9, 6.95, 0.9, 0.35, str(n), 12, color=c, align=PP_ALIGN.RIGHT)

def title(s, t, kicker=None):
    if kicker: text(s, 0.6, 0.4, 12, 0.4, kicker.upper(), 13, True, TEAL)
    text(s, 0.6, 0.75, 12.1, 0.9, t, 32, True, NAVY)

def notes(s, t): s.notes_slide.notes_text_frame.text = t

# 1 Title
s = prs.slides.add_slide(blank); bg(s, NAVY)
rect(s, 0.6, 1.0, 0.12, 2.3, ORANGE, shape=MSO_SHAPE.RECTANGLE)
text(s, 0.95, 0.95, 11.5, 1.6, "AVATAR-Twin", 60, True, WHITE)
text(s, 0.95, 2.2, 11.5, 1.2, "A hierarchical Bayesian digital twin of the astronaut bone marrow chip", 28, False, RGBColor(0xd6,0xe4,0xf0))
text(s, 0.95, 4.2, 11, 0.5, "NASA BPS Digital AVATAR Challenge", 22, True, ORANGE)
text(s, 0.95, 4.8, 11, 0.9, ["Nanthakumar R", "New Way Concepts Research"], 22, False, WHITE)
footer(s, 1, dark=True)
notes(s, "Hello. I'm Nanthakumar R from New Way Concepts Research. This is AVATAR-Twin, a digital twin of the astronaut bone marrow chip, our entry for the NASA BPS Digital AVATAR Challenge.")

# 2 Problem
s = prs.slides.add_slide(blank); bg(s, WHITE)
title(s, "One flight, few donors, one chance to learn", "The problem")
cards = [("~10 days", "Artemis II flight around the Moon; chips made from crew members' own marrow cells"),
         ("54%", "more red blood cells destroyed in space, measured in 14 astronauts on six-month missions"),
         ("Few donors", "Too few to learn personal responses from one flight alone, so the model must carry knowledge forward")]
for i, (big, small) in enumerate(cards):
    x = 0.6 + i * 4.1
    rect(s, x, 2.1, 3.9, 3.6, LIGHT)
    text(s, x + 0.25, 2.35, 3.4, 1.1, big, 44, True, [NAVY, ORANGE, TEAL][i])
    text(s, x + 0.25, 3.7, 3.4, 1.9, small, 19, False, INK)
text(s, 0.6, 6.05, 12, 0.5, "Bone marrow is among the organs most sensitive to radiation and makes every blood cell.", 18, False, GREY, italic=True)
footer(s, 2)
notes(s, "AVATAR chips are built from the cells of the crew who flew them. Bone marrow is one of the tissues most sensitive to radiation, and spaceflight already changes blood: astronauts on six-month missions destroyed 54 percent more red blood cells than normal. But one flight, a handful of donors, ten days. A single experiment cannot answer a personal question. A model has to carry what each flight teaches forward.")

# 3 Architecture
s = prs.slides.add_slide(blank); bg(s, WHITE)
title(s, "Four layers from exposure to personal prediction", "The twin")
s.shapes.add_picture(FIG + "fig_architecture.png", Inches(1.55), Inches(1.6), height=Inches(5.2))
footer(s, 3)
notes(s, "AVATAR-Twin has four layers. An exposure model turns dosimetry into biologically effective dose. A mechanistic marrow model describes stem cells, maturation, damage, repair and recovery for the red, myeloid, platelet and lymphoid lineages. A single-cell layer links multi-omic data to the rates in that model. And a hierarchical Bayesian layer splits every response into a crew-shared part and a donor-specific part.")

# 4 Shared vs individual
s = prs.slides.add_slide(blank); bg(s, WHITE)
title(s, "Every response = crew-shared effect + personal deviation", "Individual versus shared")
rect(s, 0.6, 1.9, 5.6, 2.5, LIGHT)
text(s, 0.8, 2.0, 5.2, 2.3, ["response (donor, condition)", "= donor baseline", "+ shared crew effect", "+ donor-specific deviation", "+ noise"], 20, False, NAVY)
rect(s, 0.6, 4.6, 5.6, 1.9, RGBColor(0xfd,0xf2,0xe6))
text(s, 0.8, 4.7, 5.2, 1.7, ["Individuality index, per cell type", "Near 0: the crew average fits everyone.", "Near 1: personal monitoring matters."], 19, False, INK)
s.shapes.add_picture(FIG + "fig_twin_demo.png", Inches(6.45), Inches(2.1), width=Inches(6.4))
text(s, 6.45, 5.2, 6.4, 1.2, "Synthetic demonstration: with noisy data, partial pooling lowered error (0.159 vs 0.172) and was better in 67 of 100 simulated missions.", 15, False, GREY, italic=True)
footer(s, 4)
notes(s, "That split is the heart of the idea. Each donor's response equals the shared crew effect plus a personal deviation. From it we report an individuality index for every cell type. Near zero, the crew average is a safe guide. Near one, personal monitoring matters. In a synthetic test, partial pooling reduced error when data were noisy, by pulling each estimate toward the crew average only as far as the data justify.")

# 5 Honest limits
s = prs.slides.add_slide(blank); bg(s, WHITE)
title(s, "What four donors can tell us, and how to learn more", "Honest limits")
s.shapes.add_picture(FIG + "fig_design_sensitivity.png", Inches(0.6), Inches(1.95), width=Inches(7.6))
rect(s, 8.5, 1.95, 4.25, 3.9, LIGHT)
text(s, 8.7, 2.1, 3.9, 4.3, ["Flight vs ground only: individual spread is almost unidentifiable.", "A ground dose ladder on the same donors' chips narrows it sharply.", "The twin ranks the next experiments by expected information gain."], 19, False, INK)
text(s, 0.6, 5.7, 7.6, 0.8, "Synthetic design analysis, 5,000 simulated experiments per design. True value 1.0.", 14, False, GREY, italic=True)
footer(s, 5)
notes(s, "We also tested what four donors can tell us, and the answer is honest. With flight versus ground only, the individual spread is almost impossible to estimate. Adding a ground dose ladder, the same donors' chips exposed to several radiation levels, narrows it sharply. So the twin tells NASA which experiments to run next.")

# 6 Improving + validation
s = prs.slides.add_slide(blank); bg(s, WHITE)
title(s, "It keeps improving, and it has to earn each release", "Continual learning and validation")
cols = [("Update", ["Predict each new mission first", "Then update by sequential Bayes", "Share model-level summaries, not raw personal data"], TEAL),
        ("Gate", ["Held-out donors and chips", "Interval coverage on target", "Must beat a simple linear baseline"], NAVY),
        ("Translate", ["Check chip results against the astronaut's own blood", "Use Inspiration4, Twins Study and ISS hemolysis data from around the world"], ORANGE)]
for i, (h, lines, c) in enumerate(cols):
    x = 0.6 + i * 4.1
    rect(s, x, 2.0, 3.9, 0.7, c)
    text(s, x + 0.2, 2.07, 3.5, 0.6, h, 24, True, WHITE, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, x, 2.7, 3.9, 3.0, LIGHT)
    text(s, x + 0.2, 2.9, 3.5, 2.7, lines, 20, False, INK)
footer(s, 6)
notes(s, "The twin keeps improving through sequential Bayesian updating. Each new mission is first predicted, then used to update. Candidate models pass a validation gate: held-out donors, interval coverage, and a comparison against simple linear baselines. Chip results are then checked against the astronauts' own blood, using Inspiration4, the Twins Study and ISS hemolysis data from around the world.")

# 7 Close
s = prs.slides.add_slide(blank); bg(s, NAVY)
text(s, 0.6, 0.75, 12, 0.9, "What it delivers", 34, True, WHITE)
items = ["Lineage recovery and stem reserve, with intervals", "An individuality index per cell type", "Monitoring and medical-kit planning for each crew member", "The next experiments worth running"]
text(s, 0.6, 1.9, 7.2, 3.6, items, 22, False, RGBColor(0xe3,0xec,0xf5))
rect(s, 8.2, 1.9, 4.5, 2.2, RGBColor(0x1d,0x4a,0x78))
text(s, 8.45, 2.05, 4.1, 2.0, ["White paper, slides, video and code", REPO], 18, True, WHITE)
text(s, 0.6, 5.7, 12, 0.6, "Nanthakumar R  |  New Way Concepts Research", 20, True, ORANGE)
footer(s, 7, dark=True)
notes(s, "The outputs, predicted lineage recovery, stem reserve and the individuality index, with uncertainty, help plan monitoring and medical kits for each crew member. Code, slides and the white paper are on GitHub. Thank you.")

prs.save("AVATAR-Twin_Slides.pptx"); print("saved")
