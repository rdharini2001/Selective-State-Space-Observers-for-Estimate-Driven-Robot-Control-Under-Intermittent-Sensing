import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from ssm_obs import data, train, persist
from ssm_obs.experiments import ZOO

MODELDIR = os.path.join(os.path.dirname(__file__), "..", "results", "models")
N_TRAIN = int(os.environ.get("N_TRAIN", 200))
N_STEPS = int(os.environ.get("N_STEPS", 200))
ONLY = set(sys.argv[1:])  # optionally restrict to named models

def main():
    print(f"generating training data: {N_TRAIN} x {N_STEPS}")
    t0 = time.time()
    ds = data.generate(N_TRAIN, N_STEPS, seed=1)
    val = data.generate(max(16, N_TRAIN // 12), N_STEPS, seed=2)
    print(f"  data ready in {time.time()-t0:.0f}s")
    for spec in ZOO:
        if ONLY and spec.name not in ONLY:
            continue
        path = os.path.join(MODELDIR, spec.name)
        if os.path.exists(path + ".npz"):
            print(f"[skip] {spec.name} (already trained)")
            continue
        print(f"[train] {spec.name}")
        t0 = time.time()
        p = train.train(spec, ds, val, verbose=True)
        persist.save(path, spec, p)
        print(f"  saved {spec.name} in {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
