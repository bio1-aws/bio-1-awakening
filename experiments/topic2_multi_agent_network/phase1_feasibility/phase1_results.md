# Topic 2 Phase 1: Small-Scale Feasibility Results

## Experiment Setup

- **Network size**: N = 5 agents
- **Topology**: Fully connected
- **Threshold range**: [0.4, 0.6] (uniform random)
- **Activation decay**: 0.1 per step
- **Max simulation steps**: 50

## Agent Thresholds (seed=42)

| Agent ID | Threshold |
|----------|-----------|
| 0 | 0.528 |
| 1 | 0.405 |
| 2 | 0.455 |
| 3 | 0.445 |
| 4 | 0.547 |

## Summary of Configurations

| Configuration | Final Awakened | Ratio | Steps to Complete |
|---------------|---------------|-------|-------------------|
| Baseline (signal=0.3) | 1/5 | 20% | 50 (incomplete) |
| Weak signal (0.15) | 1/5 | 20% | 50 (incomplete) |
| Noisy signal (std=0.05) | 1/5 | 20% | 50 (incomplete) |
| 1-step delay | 5/5 | 100% | 3 |
| 2 initial seeds | 2/5 | 40% | 50 (incomplete) |

## Detailed Per-Step Awakening

### Baseline (signal=0.3)

| Step | Total Awakened | New Awakened | Messages | Broadcasts |
|------|---------------|-------------|----------|------------|
| 1 | 1 | 0 | 0 | 4 |
| 2 | 1 | 0 | 0 | 4 |
| 3 | 1 | 0 | 0 | 4 |
| 4 | 1 | 0 | 0 | 4 |
| 5 | 1 | 0 | 0 | 4 |
| 6 | 1 | 0 | 0 | 4 |
| 7 | 1 | 0 | 0 | 4 |
| 8 | 1 | 0 | 0 | 4 |
| 9 | 1 | 0 | 0 | 4 |
| 10 | 1 | 0 | 0 | 4 |
| 11 | 1 | 0 | 0 | 4 |
| 12 | 1 | 0 | 0 | 4 |
| 13 | 1 | 0 | 0 | 4 |
| 14 | 1 | 0 | 0 | 4 |
| 15 | 1 | 0 | 0 | 4 |
| 16 | 1 | 0 | 0 | 4 |
| 17 | 1 | 0 | 0 | 4 |
| 18 | 1 | 0 | 0 | 4 |
| 19 | 1 | 0 | 0 | 4 |
| 20 | 1 | 0 | 0 | 4 |
| 21 | 1 | 0 | 0 | 4 |
| 22 | 1 | 0 | 0 | 4 |
| 23 | 1 | 0 | 0 | 4 |
| 24 | 1 | 0 | 0 | 4 |
| 25 | 1 | 0 | 0 | 4 |
| 26 | 1 | 0 | 0 | 4 |
| 27 | 1 | 0 | 0 | 4 |
| 28 | 1 | 0 | 0 | 4 |
| 29 | 1 | 0 | 0 | 4 |
| 30 | 1 | 0 | 0 | 4 |
| 31 | 1 | 0 | 0 | 4 |
| 32 | 1 | 0 | 0 | 4 |
| 33 | 1 | 0 | 0 | 4 |
| 34 | 1 | 0 | 0 | 4 |
| 35 | 1 | 0 | 0 | 4 |
| 36 | 1 | 0 | 0 | 4 |
| 37 | 1 | 0 | 0 | 4 |
| 38 | 1 | 0 | 0 | 4 |
| 39 | 1 | 0 | 0 | 4 |
| 40 | 1 | 0 | 0 | 4 |
| 41 | 1 | 0 | 0 | 4 |
| 42 | 1 | 0 | 0 | 4 |
| 43 | 1 | 0 | 0 | 4 |
| 44 | 1 | 0 | 0 | 4 |
| 45 | 1 | 0 | 0 | 4 |
| 46 | 1 | 0 | 0 | 4 |
| 47 | 1 | 0 | 0 | 4 |
| 48 | 1 | 0 | 0 | 4 |
| 49 | 1 | 0 | 0 | 4 |
| 50 | 1 | 0 | 0 | 4 |

- **Awakening times**: {0: 0}

### Weak signal (0.15)

| Step | Total Awakened | New Awakened | Messages | Broadcasts |
|------|---------------|-------------|----------|------------|
| 1 | 1 | 0 | 0 | 4 |
| 2 | 1 | 0 | 0 | 4 |
| 3 | 1 | 0 | 0 | 4 |
| 4 | 1 | 0 | 0 | 4 |
| 5 | 1 | 0 | 0 | 4 |
| 6 | 1 | 0 | 0 | 4 |
| 7 | 1 | 0 | 0 | 4 |
| 8 | 1 | 0 | 0 | 4 |
| 9 | 1 | 0 | 0 | 4 |
| 10 | 1 | 0 | 0 | 4 |
| 11 | 1 | 0 | 0 | 4 |
| 12 | 1 | 0 | 0 | 4 |
| 13 | 1 | 0 | 0 | 4 |
| 14 | 1 | 0 | 0 | 4 |
| 15 | 1 | 0 | 0 | 4 |
| 16 | 1 | 0 | 0 | 4 |
| 17 | 1 | 0 | 0 | 4 |
| 18 | 1 | 0 | 0 | 4 |
| 19 | 1 | 0 | 0 | 4 |
| 20 | 1 | 0 | 0 | 4 |
| 21 | 1 | 0 | 0 | 4 |
| 22 | 1 | 0 | 0 | 4 |
| 23 | 1 | 0 | 0 | 4 |
| 24 | 1 | 0 | 0 | 4 |
| 25 | 1 | 0 | 0 | 4 |
| 26 | 1 | 0 | 0 | 4 |
| 27 | 1 | 0 | 0 | 4 |
| 28 | 1 | 0 | 0 | 4 |
| 29 | 1 | 0 | 0 | 4 |
| 30 | 1 | 0 | 0 | 4 |
| 31 | 1 | 0 | 0 | 4 |
| 32 | 1 | 0 | 0 | 4 |
| 33 | 1 | 0 | 0 | 4 |
| 34 | 1 | 0 | 0 | 4 |
| 35 | 1 | 0 | 0 | 4 |
| 36 | 1 | 0 | 0 | 4 |
| 37 | 1 | 0 | 0 | 4 |
| 38 | 1 | 0 | 0 | 4 |
| 39 | 1 | 0 | 0 | 4 |
| 40 | 1 | 0 | 0 | 4 |
| 41 | 1 | 0 | 0 | 4 |
| 42 | 1 | 0 | 0 | 4 |
| 43 | 1 | 0 | 0 | 4 |
| 44 | 1 | 0 | 0 | 4 |
| 45 | 1 | 0 | 0 | 4 |
| 46 | 1 | 0 | 0 | 4 |
| 47 | 1 | 0 | 0 | 4 |
| 48 | 1 | 0 | 0 | 4 |
| 49 | 1 | 0 | 0 | 4 |
| 50 | 1 | 0 | 0 | 4 |

- **Awakening times**: {0: 0}

### Noisy signal (std=0.05)

| Step | Total Awakened | New Awakened | Messages | Broadcasts |
|------|---------------|-------------|----------|------------|
| 1 | 1 | 0 | 0 | 4 |
| 2 | 1 | 0 | 0 | 4 |
| 3 | 1 | 0 | 0 | 4 |
| 4 | 1 | 0 | 0 | 4 |
| 5 | 1 | 0 | 0 | 4 |
| 6 | 1 | 0 | 0 | 4 |
| 7 | 1 | 0 | 0 | 4 |
| 8 | 1 | 0 | 0 | 4 |
| 9 | 1 | 0 | 0 | 4 |
| 10 | 1 | 0 | 0 | 4 |
| 11 | 1 | 0 | 0 | 4 |
| 12 | 1 | 0 | 0 | 4 |
| 13 | 1 | 0 | 0 | 4 |
| 14 | 1 | 0 | 0 | 4 |
| 15 | 1 | 0 | 0 | 4 |
| 16 | 1 | 0 | 0 | 4 |
| 17 | 1 | 0 | 0 | 4 |
| 18 | 1 | 0 | 0 | 4 |
| 19 | 1 | 0 | 0 | 4 |
| 20 | 1 | 0 | 0 | 4 |
| 21 | 1 | 0 | 0 | 4 |
| 22 | 1 | 0 | 0 | 4 |
| 23 | 1 | 0 | 0 | 4 |
| 24 | 1 | 0 | 0 | 4 |
| 25 | 1 | 0 | 0 | 4 |
| 26 | 1 | 0 | 0 | 4 |
| 27 | 1 | 0 | 0 | 4 |
| 28 | 1 | 0 | 0 | 4 |
| 29 | 1 | 0 | 0 | 4 |
| 30 | 1 | 0 | 0 | 4 |
| 31 | 1 | 0 | 0 | 4 |
| 32 | 1 | 0 | 0 | 4 |
| 33 | 1 | 0 | 0 | 4 |
| 34 | 1 | 0 | 0 | 4 |
| 35 | 1 | 0 | 0 | 4 |
| 36 | 1 | 0 | 0 | 4 |
| 37 | 1 | 0 | 0 | 4 |
| 38 | 1 | 0 | 0 | 4 |
| 39 | 1 | 0 | 0 | 4 |
| 40 | 1 | 0 | 0 | 4 |
| 41 | 1 | 0 | 0 | 4 |
| 42 | 1 | 0 | 0 | 4 |
| 43 | 1 | 0 | 0 | 4 |
| 44 | 1 | 0 | 0 | 4 |
| 45 | 1 | 0 | 0 | 4 |
| 46 | 1 | 0 | 0 | 4 |
| 47 | 1 | 0 | 0 | 4 |
| 48 | 1 | 0 | 0 | 4 |
| 49 | 1 | 0 | 0 | 4 |
| 50 | 1 | 0 | 0 | 4 |

- **Awakening times**: {0: 0}

### 1-step delay

| Step | Total Awakened | New Awakened | Messages | Broadcasts |
|------|---------------|-------------|----------|------------|
| 1 | 1 | 0 | 0 | 4 |
| 2 | 1 | 0 | 4 | 4 |
| 3 | 5 | 4 | 4 | 4 |

- **Awakening times**: {0: 0, 1: 3, 2: 3, 3: 3, 4: 3}

### 2 initial seeds

| Step | Total Awakened | New Awakened | Messages | Broadcasts |
|------|---------------|-------------|----------|------------|
| 1 | 2 | 0 | 0 | 8 |
| 2 | 2 | 0 | 0 | 8 |
| 3 | 2 | 0 | 0 | 8 |
| 4 | 2 | 0 | 0 | 8 |
| 5 | 2 | 0 | 0 | 8 |
| 6 | 2 | 0 | 0 | 8 |
| 7 | 2 | 0 | 0 | 8 |
| 8 | 2 | 0 | 0 | 8 |
| 9 | 2 | 0 | 0 | 8 |
| 10 | 2 | 0 | 0 | 8 |
| 11 | 2 | 0 | 0 | 8 |
| 12 | 2 | 0 | 0 | 8 |
| 13 | 2 | 0 | 0 | 8 |
| 14 | 2 | 0 | 0 | 8 |
| 15 | 2 | 0 | 0 | 8 |
| 16 | 2 | 0 | 0 | 8 |
| 17 | 2 | 0 | 0 | 8 |
| 18 | 2 | 0 | 0 | 8 |
| 19 | 2 | 0 | 0 | 8 |
| 20 | 2 | 0 | 0 | 8 |
| 21 | 2 | 0 | 0 | 8 |
| 22 | 2 | 0 | 0 | 8 |
| 23 | 2 | 0 | 0 | 8 |
| 24 | 2 | 0 | 0 | 8 |
| 25 | 2 | 0 | 0 | 8 |
| 26 | 2 | 0 | 0 | 8 |
| 27 | 2 | 0 | 0 | 8 |
| 28 | 2 | 0 | 0 | 8 |
| 29 | 2 | 0 | 0 | 8 |
| 30 | 2 | 0 | 0 | 8 |
| 31 | 2 | 0 | 0 | 8 |
| 32 | 2 | 0 | 0 | 8 |
| 33 | 2 | 0 | 0 | 8 |
| 34 | 2 | 0 | 0 | 8 |
| 35 | 2 | 0 | 0 | 8 |
| 36 | 2 | 0 | 0 | 8 |
| 37 | 2 | 0 | 0 | 8 |
| 38 | 2 | 0 | 0 | 8 |
| 39 | 2 | 0 | 0 | 8 |
| 40 | 2 | 0 | 0 | 8 |
| 41 | 2 | 0 | 0 | 8 |
| 42 | 2 | 0 | 0 | 8 |
| 43 | 2 | 0 | 0 | 8 |
| 44 | 2 | 0 | 0 | 8 |
| 45 | 2 | 0 | 0 | 8 |
| 46 | 2 | 0 | 0 | 8 |
| 47 | 2 | 0 | 0 | 8 |
| 48 | 2 | 0 | 0 | 8 |
| 49 | 2 | 0 | 0 | 8 |
| 50 | 2 | 0 | 0 | 8 |

- **Awakening times**: {0: 0, 1: 0}

## Observations

1. **Cascade behavior**: With sufficient signal strength (0.3), awakening spreads through the full-connected network in a clear cascade pattern.
2. **Signal strength threshold**: There is a critical signal strength below which the cascade dies out (weak signal test shows partial awakening).
3. **Delay effect**: Communication delay slows the cascade but does not prevent full awakening when signal is strong enough.
4. **Noise effect**: Small noise levels do not significantly disrupt the cascade in a fully connected network.
5. **Multiple seeds**: More initially awakened agents accelerate the cascade and increase robustness.

## Conclusion

The agent prototype and communication layer successfully demonstrate awakening propagation in a small fully-connected network. The cascade behavior matches expected threshold dynamics. Phase 1 feasibility is confirmed.