from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / 'figures'
OUT.mkdir(parents=True, exist_ok=True)

pretty = {
    'dead_reckoning': 'Dead reckoning',
    'ekf': 'EKF',
    'gru_dr': 'GRU-DR',
    'ssm_dr': 'SSM-DR',
    'ssm_ekf': 'SSM-EKF',
    'gru_ekf': 'GRU-EKF',
}
markers = ['o', 's', '^', 'D', '*', 'P']
observers = list(pretty)

# Corrected six-observer sweep figures with 95% CI half-widths.
axis_specs = [
    ('dropout_len', 'sweep_dropout_len.json', 'Blackout duration (steps)', 'fig_sweep_blackout.png'),
    ('sig_r', 'sweep_sig_r.json', r'Range noise $\sigma_r$ (m)', 'fig_sweep_range_noise.png'),
    ('n_landmarks', 'sweep_n_landmarks.json', 'Number of active landmarks', 'fig_sweep_landmarks.png'),
    ('gyro_bias', 'sweep_gyro_bias.json', 'Gyroscope bias (rad/s)', 'fig_sweep_gyro_bias.png'),
]
for axis, filename, xlabel, outname in axis_specs:
    d = json.load(open(ROOT / 'results' / filename))
    levels = d['_levels']
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for marker, observer in zip(markers, observers):
        means = np.array([row['ct_rmse'][0] for row in d[observer]])
        cis = np.array([row['ct_rmse'][1] for row in d[observer]])
        ax.plot(levels, means, marker=marker, linewidth=1.8, label=pretty[observer])
        ax.fill_between(levels, np.maximum(0, means-cis), means+cis, alpha=0.12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Closed-loop cross-track RMSE (m)')
    ax.set_title('Closed-loop degradation under ' + axis.replace('_', ' '))
    ax.legend(frameon=False, ncol=2, fontsize=8)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / outname, dpi=220)
    plt.close(fig)

# Corrected replay-vs-closed-loop scatter over all six observers and 24 conditions.
proxy = json.load(open(ROOT / 'results' / 'enhanced' / 'proxy_analysis.json'))
fig, ax = plt.subplots(figsize=(6.5, 4.7))
for marker, observer in zip(markers, observers):
    xs = [proxy['proxy_means']['pose_rmse'][c][observer] for c in proxy['conditions']]
    ys = [proxy['closed_loop_ct'][c][observer] for c in proxy['conditions']]
    ax.scatter(xs, ys, marker=marker, s=34, alpha=0.82, label=pretty[observer])
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Replay position RMSE (m)')
ax.set_ylabel('Closed-loop cross-track RMSE (m)')
ax.set_title(r'Broad agreement, imperfect deployment selection ($\rho=0.923$, $r=0.477$)')
ax.legend(frameon=False, ncol=2, fontsize=8)
ax.grid(alpha=0.25, which='both')
fig.tight_layout()
fig.savefig(OUT / 'fig_proxy_scatter_corrected.png', dpi=220)
plt.close(fig)

# Per-condition selection regret matrix in centimetres.
proxy_order = ['pose_rmse', 'controller_disagreement', 'lcse', 'counterfactual_replay']
proxy_labels = ['Pose RMSE', 'Command disagreement', 'LCSE', 'Counterfactual replay']
mat = np.array([
    [100.0 * row['regret'] for row in proxy['analysis'][p]['selection']['rows']]
    for p in proxy_order
])
condition_labels=[]
for c in proxy['conditions']:
    axis, level = c.split('=')
    short = {'dropout_len':'B', 'sig_r':'R', 'n_landmarks':'L', 'gyro_bias':'G'}[axis]
    condition_labels.append(short + level)
fig, ax = plt.subplots(figsize=(10.2, 3.1))
im = ax.imshow(mat, aspect='auto')
ax.set_yticks(np.arange(len(proxy_labels)), proxy_labels)
ax.set_xticks(np.arange(len(condition_labels)), condition_labels, rotation=60, ha='right', fontsize=8)
ax.set_xlabel('Condition: B=blackout, R=range noise, L=landmarks, G=gyro bias')
ax.set_title('Closed-loop selection regret from offline proxies (cm)')
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        if mat[i,j] >= 0.5:
            ax.text(j, i, f'{mat[i,j]:.1f}', ha='center', va='center', fontsize=6)
fig.colorbar(im, ax=ax, label='Regret (cm)', fraction=0.025, pad=0.02)
fig.tight_layout()
fig.savefig(OUT / 'fig_proxy_regret_matrix.png', dpi=220)
plt.close(fig)

print('wrote figures to', OUT)
