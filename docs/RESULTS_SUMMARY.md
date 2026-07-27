# Audited results summary

## Observer selection across 24 synthetic conditions

| Offline proxy | Global Spearman | Top-1 failures | Mean regret (m) | Max regret (m) |
|---|---:|---:|---:|---:|
| Position RMSE | 0.923 | 5/24 | 0.0051 | 0.0347 |
| Command disagreement | 0.876 | 13/24 | 0.0188 | 0.1208 |
| Local control sensitivity | 0.903 | 3/24 | 0.0051 | 0.0940 |
| Counterfactual error replay | 0.842 | 14/24 | 0.0159 | 0.0474 |

LCSE has fewer observed top-1 failures than pose RMSE, but a condition bootstrap gives a flip-reduction
95% interval of -0.125 to 0.292. The evidence does not justify claiming a definitive replacement metric.

## Matched EKF-anchor ablation: closed-loop cross-track RMSE (m)

| Condition | Selective + mask | Non-selective + mask | Selective, no mask |
|---|---:|---:|---:|
| Nominal | 0.199 | 0.203 | 0.195 |
| Long blackout | 0.336 | 0.235 | 0.308 |
| High range noise | 0.307 | 0.322 | 0.294 |
| Two landmarks | 0.289 | 0.235 | 0.274 |
| High gyro bias | 0.314 | 0.393 | 0.312 |

Selectivity is regime-dependent. The non-selective model improves long-blackout and sparse-landmark
tracking but degrades high-bias tracking. Mask removal is usually close to the selective model.

## SSM-EKF training-seed range

| Condition | Minimum | Maximum | Across-seed SD |
|---|---:|---:|---:|
| Nominal | 0.189 | 0.199 | 0.006 |
| Long blackout | 0.231 | 0.336 | 0.060 |
| High range noise | 0.249 | 0.307 | 0.033 |
| Two landmarks | 0.226 | 0.289 | 0.032 |
| High gyro bias | 0.293 | 0.314 | 0.011 |

## Secondary-controller sensitivity

A matched five-seed evaluation with pure pursuit and Kanayama uses the same plant, observers, conditions, actuator limits, and random seeds. The closed-loop oracle changes in 8/24 conditions (33.3%). Replay position RMSE misselects the Kanayama observer in 7/24 conditions (29.2%), with mean regret 0.0142 m and maximum regret 0.0923 m. A paired seed bootstrap gives a wide 95% interval of 0.208-0.625 for the controller-oracle change fraction. Treat this as a secondary sensitivity, not a replacement for the primary 10-seed analysis.

## UTIAS MRCLAM

On a 600 s Robot 1 segment, the 15-landmark dead-reckoning RMSE is 3.392 m. The best tested EKF
covariance setting reaches 1.357 m. In the intentionally difficult eight-landmark zero-shot transfer,
SSM-EKF and GRU-EKF reach 2.625 m and 2.597 m position RMSE, respectively, but both worsen heading
RMSE relative to DR. This is evidence that the current ordered-slot representation is not a robust
map-generalizing observer.
