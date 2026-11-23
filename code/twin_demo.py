"""Minimal synthetic demonstration of the AVATAR-Twin idea.

1. A semi-mechanistic marrow model (proliferating pool -> 3 transit stages -> circulating
   output, with feedback) is perturbed by a radiation pulse.
2. Each donor has their own radiosensitivity k_d = exp(mu + u_d).
3. Per-chip fits are combined by partial pooling (empirical Bayes), compared with fitting
   each donor alone and with ignoring donor differences.

Everything here is SYNTHETIC.  It illustrates the method; it is not AVATAR data.
Run: python twin_demo.py [noise]   (default noise 0.20; try 0.5)
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


T = np.array([0, 2, 4, 6, 8, 10, 14, 18, 21.0])      # days on chip
MTT, GAMMA, KPROL0 = 4.0, 0.2, 4.0 / 4.0              # mean transit time, feedback power

def marrow(k, dose, t=T):
    """Friberg-type model. State: proliferating P, transit T1..T3, circulating C (baseline 1)."""
    ktr = 4.0 / MTT
    def f(_, y):
        P, T1, T2, T3, C = y
        fb = (1.0 / max(C, 1e-6)) ** GAMMA
        kill = k * dose * np.exp(-_ / 3.0)                # radiation effect fades over days
        dP = ktr * P * fb * (1 - kill) - ktr * P
        return [dP, ktr * (P - T1), ktr * (T1 - T2), ktr * (T2 - T3), ktr * (T3 - C)]
    s = solve_ivp(f, [0, t[-1]], [1, 1, 1, 1, 1], t_eval=t, rtol=1e-6, atol=1e-8)
    return s.y[4]

# ---- simulate + fit (wrapped so it can be repeated)
import sys
NOISE = float(sys.argv[1]) if len(sys.argv) > 1 else 0.20   # measurement noise (log scale)
mu, tau, noise = np.log(0.35), 0.25, NOISE
doses = [0.0, 1.0, 2.0]
D, R = 4, 2

def run(seed, keep=False):
    rng = np.random.default_rng(seed)
    u = rng.normal(0, tau, D); k_true = np.exp(mu + u)
    data = {}
    for d in range(D):
        for r in range(R):
            for g in doses:
                data[(d, r, g)] = np.log(marrow(k_true[d], g)) + rng.normal(0, noise, len(T))
    def fit_chip(d, r):
        def res(p):
            return np.concatenate([np.log(marrow(np.exp(p[0]), g)) - data[(d, r, g)] for g in doses[1:]])
        return least_squares(res, [np.log(0.3)], bounds=(-5, 1)).x[0]
    est = np.array([[fit_chip(d, r) for r in range(R)] for d in range(D)])
    dm = est.mean(1)
    sw2 = est.var(1, ddof=1).mean() / R
    gm = dm.mean()
    tau2 = max(dm.var(ddof=1) - sw2, 1e-6)
    w = tau2 / (tau2 + sw2)
    pp = gm + w * (dm - gm)
    truth = mu + u
    rm = lambda x: np.sqrt(np.mean((x - truth) ** 2))
    out = (rm(dm), rm(np.full(D, gm)), rm(pp), w)
    return (out, data, dm, pp, gm, truth) if keep else out

res = np.array([run(s) for s in range(100)])
print("Mean over 100 simulated missions (4 donors, 2 chips each):")
print("  RMSE of log-radiosensitivity  donor alone %.3f | crew average only %.3f | partial pooling %.3f" % tuple(res[:, :3].mean(0)))
print("  partial pooling beat donor-alone in %d of 100 runs; mean shrinkage weight %.2f" % ((res[:, 2] < res[:, 0]).sum(), res[:, 3].mean()))
_, data, dm, pp, gm, truth = run(3, keep=True)

# ---- figure
fig, ax = plt.subplots(1, 2, figsize=(8, 3.4), dpi=200)
cols = ["#1f4e79", "#c0392b", "#2e8b57", "#b9770e"]
for d in range(D):
    ax[0].plot(T, np.exp(data[(d, 0, 1.0)]), "o", ms=3, color=cols[d], alpha=.6)
    ax[0].plot(T, marrow(np.exp(pp[d]), 1.0), "-", color=cols[d], lw=1.4, label="donor %d" % (d + 1))
ax[0].set_xlabel("days on chip"); ax[0].set_ylabel("output relative to baseline")
ax[0].set_title("1 Gy exposure: data (dots), twin fit (lines)", fontsize=9); ax[0].legend(fontsize=7)
x = np.arange(D)
ax[1].plot(x, truth, "k*", ms=9, label="truth")
ax[1].plot(x - .12, dm, "s", color="#7f8c8d", label="donor alone")
ax[1].plot(x + .12, pp, "o", color="#1f4e79", label="partial pooling")
ax[1].axhline(gm, color="#c0392b", ls=":", lw=1, label="crew average")
ax[1].set_xticks(x); ax[1].set_xticklabels(["donor %d" % (i + 1) for i in x], fontsize=8)
ax[1].set_ylabel("log radiosensitivity"); ax[1].legend(fontsize=7)
ax[1].set_title("Shared level + individual deviation", fontsize=9)
for a in ax: a.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("../figures/fig_twin_demo.png")
