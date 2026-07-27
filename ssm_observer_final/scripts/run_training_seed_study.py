#!/usr/bin/env python3
"""Train and evaluate multiple initialization seeds for the two EKF hybrids."""
from __future__ import annotations
import json, os, sys, copy
from pathlib import Path
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","src"))
import numpy as np
from ssm_obs import data, experiments as E, persist, torch_train

ROOT=Path(__file__).resolve().parents[1]
MODELS=["ssm_ekf","gru_ekf"];SEEDS=[0,1,2]


def mean_ci(x):
    a=np.asarray(x,float);return [float(a.mean()),float(1.96*a.std(ddof=1)/np.sqrt(len(a)))]


def main():
    specs={s.name:s for s in E.ZOO};ds=data.generate(200,200,seed=1);val=data.generate(16,200,seed=2)
    paths={}
    for name in MODELS:
        for sd in SEEDS:
            if sd==0:
                path=ROOT/"results"/"models"/name
            else:
                spec=copy.copy(specs[name]);spec.seed=sd;spec.name=f"{name}_seed{sd}"
                path=ROOT/"results"/"models_multiseed"/spec.name
                if not path.with_suffix(".npz").exists():
                    print("training",spec.name,flush=True);p=torch_train.train(spec,ds,val,verbose=True);persist.save(str(path),spec,p)
            paths[(name,sd)]=path
    conditions={"nominal":E.nominal_eval(),
        "long_blackout":E._apply(E.nominal_eval(),"dropout_len",34),
        "high_range_noise":E._apply(E.nominal_eval(),"sig_r",.5),
        "two_landmarks":E._apply(E.nominal_eval(),"n_landmarks",2),
        "high_gyro_bias":E._apply(E.nominal_eval(),"gyro_bias",.25)}
    result={"training_seeds":SEEDS,"models":MODELS,"conditions":{}}
    for label,p in conditions.items():
        print("evaluate",label,flush=True);result["conditions"][label]={}
        for name in MODELS:
            result["conditions"][label][name]={}
            train_seed_means=[]
            for sd in SEEDS:
                spec,w=persist.load(str(paths[(name,sd)]));trained={name:(spec,w)}
                vals=E.eval_closed(name,trained,p,list(range(10)))
                ct=[v["ct_rmse"] for v in vals];train_seed_means.append(float(np.mean(ct)))
                result["conditions"][label][name][str(sd)]={"ct_rmse":mean_ci(ct),"seed_values":ct}
            result["conditions"][label][name]["across_training_seeds"]={
                "mean":float(np.mean(train_seed_means)),"std":float(np.std(train_seed_means,ddof=1)),
                "min":float(np.min(train_seed_means)),"max":float(np.max(train_seed_means)),
                "values":train_seed_means}
        out=ROOT/"results"/"enhanced"/"training_seed_study.json";out.parent.mkdir(parents=True,exist_ok=True);json.dump(result,open(out,"w"),indent=2)
    print(json.dumps({c:{m:result['conditions'][c][m]['across_training_seeds'] for m in MODELS} for c in conditions},indent=2))

if __name__=="__main__":main()
