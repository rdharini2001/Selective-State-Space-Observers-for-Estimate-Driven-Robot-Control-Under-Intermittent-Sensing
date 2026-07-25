"""Geometric tracking controllers.  Each returns u=[v, omega] given the
current (estimated) pose.  Closing the loop on the ESTIMATE is what makes
the estimator's error structure matter."""
import numpy as np
from . import dynamics as dyn


class PurePursuit:
    """Pure-pursuit steering at constant speed along a fixed path P (N,2).

    Reference: Coulter, CMU-RI-TR-92-01.  Curvature to a look-ahead point:
        kappa = 2 sin(alpha) / Ld ,   omega = v * kappa
    Steering depends directly on the estimated heading -> heading error
    translates straight into cross-track error.
    """
    def __init__(self, P, v_cmd=1.0, Ld=0.8):
        self.P = P
        self.v = v_cmd
        self.Ld = Ld
        self._i = 0

    def __call__(self, pose, k):
        x, y, th = pose
        # advance the target index to the first point >= Ld ahead
        i = self._i
        N = len(self.P)
        while i < N - 1 and np.hypot(*(self.P[i] - [x, y])) < self.Ld:
            i += 1
        self._i = i
        gx, gy = self.P[i]
        alpha = dyn.wrap(np.arctan2(gy - y, gx - x) - th)
        kappa = 2.0 * np.sin(alpha) / self.Ld
        return np.array([self.v, self.v * kappa])


class Kanayama:
    """Kanayama et al. (ICRA 1990) posture-tracking controller.

    Uses a time-indexed reference (P, theta_ref, v_ref, w_ref).  Error is
    expressed in the robot frame of the ESTIMATED pose.
    """
    def __init__(self, ref, Kx=1.5, Ky=6.0, Kth=3.0):
        self.P, self.th_ref, self.v_ref, self.w_ref = ref
        self.Kx, self.Ky, self.Kth = Kx, Ky, Kth

    def __call__(self, pose, k):
        k = min(k, len(self.P) - 1)
        x, y, th = pose
        xr, yr = self.P[k]; thr = self.th_ref[k]
        c, s = np.cos(th), np.sin(th)
        ex = c * (xr - x) + s * (yr - y)
        ey = -s * (xr - x) + c * (yr - y)
        eth = dyn.wrap(thr - th)
        v = self.v_ref[k] * np.cos(eth) + self.Kx * ex
        w = self.w_ref[k] + self.v_ref[k] * (self.Ky * ey + self.Kth * np.sin(eth))
        return np.array([v, w])
