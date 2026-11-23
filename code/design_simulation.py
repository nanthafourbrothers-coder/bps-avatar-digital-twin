"""Design-sensitivity simulation.

Question: with D donors, S exposure conditions (ground control included) and R replicate
chips per donor x condition, how well can we estimate the SD of donor-specific response
differences (sigma_b)?  Balanced two-way random-effects design, method-of-moments estimate.
All numbers are synthetic and illustrative.  Run: python design_simulation.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)

def estimate_sigma_b(D, S, R, sb=1.0, se=1.0, sa=1.5):
    a = rng.normal(0, sa, (D, 1, 1))          # donor baseline (removed by ground control)
    beta = rng.normal(0, 1, (1, S, 1))        # shared condition effects
    b = rng.normal(0, sb, (D, S, 1))          # donor-specific response differences
    y = a + beta + b + rng.normal(0, se, (D, S, R))
    cm = y.mean(2)
    inter = cm - cm.mean(1, keepdims=True) - cm.mean(0, keepdims=True) + cm.mean()
    ms_int = R * (inter ** 2).sum() / ((D - 1) * (S - 1))
    ms_e = ((y - cm[:, :, None]) ** 2).sum() / (D * S * (R - 1))
    return max(0.0, (ms_int - ms_e) / R) ** 0.5

designs = [(4, 2, 3), (4, 4, 3), (4, 7, 3), (8, 4, 3), (16, 4, 3), (16, 7, 3)]
rows = []
for D, S, R in designs:
    v = np.array([estimate_sigma_b(D, S, R) for _ in range(5000)])
    rows.append((D, S, R, *np.percentile(v, [5, 50, 95])))

print("D  S  R   p5    median  p95   (true sigma_b = 1.0)")
for r in rows:
    print("%2d %2d %2d  %.2f  %.2f   %.2f" % r)

fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=200)
labels = ["%d donors\n%d conditions" % (r[0], r[1]) for r in rows]
x = np.arange(len(rows))
ax.vlines(x, [r[3] for r in rows], [r[5] for r in rows], color="#1f4e79", lw=6, alpha=.35)
ax.plot(x, [r[4] for r in rows], "o", color="#1f4e79")
ax.axhline(1.0, color="#c0392b", ls="--", lw=1)
ax.text(len(rows) - .6, 1.03, "true value", color="#c0392b", fontsize=8, ha="right")
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=7.5)
ax.set_ylabel("estimated individual-response SD", fontsize=9)
ax.set_title("What can a handful of donors tell us? (5th-95th percentile, 3 chips per cell)", fontsize=9.5)
ax.set_ylim(0, 2); ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("../figures/fig_design_sensitivity.png")
