from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent/'figures'
pretty={'dead_reckoning':'DR','ekf':'EKF','gru_dr':'GRU-DR','ssm_dr':'SSM-DR','ssm_ekf':'SSM-EKF','gru_ekf':'GRU-EKF'}
markers=['o','s','^','D','*','P']
obs=list(pretty)
axis_specs=[
('dropout_len','sweep_dropout_len.json','Blackout duration (steps)','fig_sweep_blackout_compact.png',True),
('sig_r','sweep_sig_r.json',r'Range noise $\sigma_r$ (m)','fig_sweep_range_noise_compact.png',False),
('n_landmarks','sweep_n_landmarks.json','Active landmarks','fig_sweep_landmarks_compact.png',False),
('gyro_bias','sweep_gyro_bias.json','Gyro bias (rad/s)','fig_sweep_gyro_bias_compact.png',False)]
for axis,fn,xlab,outname,legend in axis_specs:
 d=json.load(open(ROOT/'results'/fn)); levels=d['_levels']
 fig,ax=plt.subplots(figsize=(5.8,2.65))
 for m,o in zip(markers,obs):
  means=np.array([r['ct_rmse'][0] for r in d[o]]); cis=np.array([r['ct_rmse'][1] for r in d[o]])
  ax.plot(levels,means,marker=m,linewidth=1.45,markersize=4,label=pretty[o])
  ax.fill_between(levels,np.maximum(0,means-cis),means+cis,alpha=.10)
 ax.set_xlabel(xlab,fontsize=9); ax.set_ylabel('Cross-track RMSE (m)',fontsize=9)
 ax.tick_params(labelsize=8); ax.grid(alpha=.2)
 if legend: ax.legend(frameon=False,ncol=3,fontsize=7,loc='upper left')
 fig.tight_layout(pad=.4); fig.savefig(OUT/outname,dpi=220,bbox_inches='tight'); plt.close(fig)

p=json.load(open(ROOT/'results/enhanced/proxy_analysis.json'))
fig,ax=plt.subplots(figsize=(5.8,3.3))
for m,o in zip(markers,obs):
 xs=[p['proxy_means']['pose_rmse'][c][o] for c in p['conditions']]
 ys=[p['closed_loop_ct'][c][o] for c in p['conditions']]
 ax.scatter(xs,ys,marker=m,s=24,alpha=.8,label=pretty[o])
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlabel('Replay position RMSE (m)',fontsize=9); ax.set_ylabel('Closed-loop cross-track RMSE (m)',fontsize=9)
ax.tick_params(labelsize=8); ax.grid(alpha=.2,which='both'); ax.legend(frameon=False,ncol=2,fontsize=7)
ax.text(.02,.97,r'$\rho=0.923,\ r=0.477$',transform=ax.transAxes,va='top',fontsize=9)
fig.tight_layout(pad=.4); fig.savefig(OUT/'fig_proxy_scatter_compact.png',dpi=220,bbox_inches='tight'); plt.close(fig)

order=['pose_rmse','heading_rmse','controller_disagreement','lcse','counterfactual_replay']
labels=['Pose RMSE','Heading RMSE','Command diff.','LCSE','CF replay']
vals=[100*p['analysis'][k]['selection']['flip_fraction'] for k in order]
fig,ax=plt.subplots(figsize=(5.8,3.3)); bars=ax.bar(labels,vals)
ax.set_ylabel('Top-1 failures (%)',fontsize=9); ax.tick_params(axis='x',labelrotation=20,labelsize=8); ax.tick_params(axis='y',labelsize=8); ax.set_ylim(0,100)
for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+2,f'{v:.1f}',ha='center',fontsize=7)
fig.tight_layout(pad=.4); fig.savefig(OUT/'fig_proxy_failures_compact.png',dpi=220,bbox_inches='tight'); plt.close(fig)

abl=json.load(open(ROOT/'results/enhanced/matched_ekf_ablation.json'))
conds=['nominal','long_blackout','high_range_noise','two_landmarks','high_gyro_bias']; clabs=['Nominal','Blackout','Noise','2 LM','Bias']
models=['ssm_ekf','ssm_ekf_nosel','ssm_ekf_nomask']; mlabs=['Sel.+mask','Non-selective','No global mask']
x=np.arange(len(conds)); w=.24
fig,ax=plt.subplots(figsize=(5.8,3.15))
for i,(m,l) in enumerate(zip(models,mlabs)):
 vals=[abl['conditions'][c][m]['ct_rmse'][0] for c in conds]
 ax.bar(x+(i-1)*w,vals,w,label=l)
ax.set_xticks(x,clabs,fontsize=8); ax.set_ylabel('Cross-track RMSE (m)',fontsize=9); ax.tick_params(axis='y',labelsize=8); ax.legend(frameon=False,ncol=3,fontsize=7)
fig.tight_layout(pad=.4); fig.savefig(OUT/'fig_ablation_compact.png',dpi=220,bbox_inches='tight'); plt.close(fig)

seed=json.load(open(ROOT/'results/enhanced/ssm_training_seed_eval.json'))
fig,ax=plt.subplots(figsize=(5.8,3.15))
for s in ['0','1','2']:
 vals=[seed['conditions'][c][s]['mean'] for c in conds]
 ax.plot(clabs,vals,marker='o',linewidth=1.5,label='Seed '+s)
ax.set_ylabel('Cross-track RMSE (m)',fontsize=9); ax.tick_params(labelsize=8); ax.legend(frameon=False,ncol=3,fontsize=7); ax.grid(alpha=.2)
fig.tight_layout(pad=.4); fig.savefig(OUT/'fig_seed_compact.png',dpi=220,bbox_inches='tight'); plt.close(fig)
