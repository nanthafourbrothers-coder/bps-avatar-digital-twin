import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(10, 5.4), dpi=200)
ax.set_xlim(0, 100); ax.set_ylim(0, 56); ax.axis("off")
NAVY, TEAL, ORANGE, GREY, LIGHT = "#12355b", "#1b7f8c", "#d9822b", "#5d6d7e", "#eef3f8"

def box(x, y, w, h, title, lines, fc=LIGHT, ec=NAVY, tc=NAVY):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=1.2", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h - 2.3, title, ha="center", va="top", fontsize=9.2, fontweight="bold", color=tc)
    for i, l in enumerate(lines):
        ax.text(x + w / 2, y + h - 5.6 - i * 2.7, l, ha="center", va="top", fontsize=7.4, color="#222")

def arrow(x1, y1, x2, y2, c=GREY, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=10, color=c, lw=1.3, linestyle=ls))

ax.text(50, 54.3, "AVATAR-Twin: layers and data flow", ha="center", fontsize=12, fontweight="bold", color=NAVY)

# inputs
box(1, 37, 21, 13, "Exposure inputs", ["dose, dose rate, LET mix", "microgravity, launch, handling", "(Orion detectors, ground beams)"], fc="#fdf2e6", ec=ORANGE, tc="#8a4b0f")
box(1, 21, 21, 13, "Donor baseline", ["pre-flight blood counts", "age, sex, genotype, CHIP", "ground-control chip"], fc="#fdf2e6", ec=ORANGE, tc="#8a4b0f")
box(1, 5, 21, 13, "Chip and blood readouts", ["single-cell RNA, cell counts", "cytokines, proteins", "pre/post-flight blood"], fc="#fdf2e6", ec=ORANGE, tc="#8a4b0f")

# layers
box(30, 37, 24, 13, "1  Exposure model", ["physical dose to biologically", "effective dose per chip", "(with uncertainty)"])
box(30, 21, 24, 13, "2  Mechanistic marrow core", ["stem pool, maturation stages,", "damage, repair, feedback", "red / myeloid / platelet / lymphoid"], ec=TEAL, tc=TEAL)
box(30, 5, 24, 13, "3  Cell-state layer", ["factor model over omics views", "pseudobulk per donor and cell type", "links cell states to model rates"])
box(62, 21, 17, 29, "4  Hierarchical Bayes", ["response = crew-shared", "effect + donor-specific", "deviation", "", "individuality index", "per cell type / program"], ec=NAVY, tc=NAVY)

# outputs
box(85, 33, 14.5, 17, "Predictions", ["lineage output,", "stem reserve,", "recovery time,", "with intervals"], fc="#e8f5ee", ec="#2e7d4f", tc="#1f6b3d")
box(85, 13, 14.5, 17, "Decisions", ["monitoring plan", "medical-kit mix", "next chips and", "ground tests"], fc="#e8f5ee", ec="#2e7d4f", tc="#1f6b3d")

for y in (43.5, 27.5, 11.5):
    arrow(22.3, y, 29.7, y)
arrow(54.3, 43.5, 61.7, 40); arrow(54.3, 27.5, 61.7, 31); arrow(54.3, 11.5, 61.7, 25)
arrow(42, 36.7, 42, 34.3); arrow(42, 20.7, 42, 18.3, style="<|-|>")
arrow(79.3, 40, 84.7, 41); arrow(79.3, 30, 84.7, 22)

# update loop
ax.add_patch(FancyBboxPatch((62, 2), 37, 7.5, boxstyle="round,pad=0.25,rounding_size=1.2", fc="#fff", ec=NAVY, lw=1.2, ls="--"))
ax.text(80.5, 7.4, "Continual loop", ha="center", fontsize=8.6, fontweight="bold", color=NAVY)
ax.text(80.5, 4.2, "new data > Bayesian update > validation gate > new release", ha="center", fontsize=7, color="#222")
arrow(92, 12.7, 92, 9.8, c=NAVY, ls="--")
plt.savefig("../figures/fig_architecture.png", bbox_inches="tight", facecolor="white")
