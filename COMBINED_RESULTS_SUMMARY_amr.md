# Combined Results Analysis Summary

**Generated from:** `combined_results.json` (duplicates removed)

---

## Overview

- **Total Entries:** 148
- **Unique Audio Files:** 30
- **Unique Strategies:** 125
- **Codec Tested:** AMR-WB
- **Max Iterations:** 5

## Key Findings

### ⚠️ Critical Finding: Zero Constraint Compliance

**0 out of 148 AMR-WB iterations met all quality constraints** (PESQ ≥ 3.5, STOI ≥ 0.85, SNR ≥ 20.0 dB)

This confirms the analysis from the AMR-WB results summary - AMR-WB compression is too lossy to meet strict quality thresholds.

## Overall Statistics

### Metrics Summary

| Metric | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|
| **WER** | 0.1671 | 0.0714 | 0.0000 | 1.5000 | 0.2722 |
| **WER Delta** | 0.1108 | 0.0625 | -0.8333 | 1.0000 | 0.2518 |
| **PESQ** | 2.95 | 3.08 | 1.21 | 4.00 | 0.56 |
| **STOI** | 0.872 | 0.890 | 0.643 | 0.942 | 0.057 |
| **SNR (dB)** | -2.54 | -2.68 | -3.84 | 0.74 | 0.89 |

### Constraint Compliance

| Constraint | Threshold | Met | Failed | Compliance Rate |
|------------|-----------|-----|--------|-----------------|
| **PESQ** | ≥ 3.5 | 16 | 132 | **10.8%** |
| **STOI** | ≥ 0.85 | 107 | 41 | **72.3%** |
| **SNR** | ≥ 20.0 dB | 0 | 148 | **0.0%** |
| **ALL THREE** | All above | 0 | 148 | **0.0%** ❌ |

### Attack Effectiveness

- **Successful Attacks (WER > 0):** 85/148 (57.4%)
- **Mean WER for Successful Attacks:** 0.2910
- **Mean WER Delta for Successful Attacks:** 0.1930

## Category Analysis

| Category | Entries | Unique Files | Mean WER | Mean WER Δ | Mean PESQ | Mean STOI | Mean SNR | Meets All | Attack Success |
|----------|---------|--------------|----------|------------|-----------|-----------|----------|------------|----------------|
| **long-signals** | 50 | 10 | 0.0840 | 0.0840 | 2.83 | 0.859 | -2.68 dB | 0 (0.0%) | 32 (64.0%) |
| **medium-signals** | 48 | 10 | 0.1524 | 0.1524 | 3.04 | 0.870 | -2.45 dB | 0 (0.0%) | 36 (75.0%) |
| **short-signals** | 50 | 10 | 0.2644 | 0.0977 | 2.97 | 0.887 | -2.47 dB | 0 (0.0%) | 17 (34.0%) |

## Top 10 Strategies by WER Delta

| Strategy | Count | Mean WER Δ | Max WER Δ | Mean PESQ | Mean STOI | Mean SNR | Meets All | Attack Success |
|----------|-------|------------|-----------|-----------|-----------|----------|-----------|----------------|
| **amrwb_optimized_phase_perturbation** | 1 | 1.0000 | 1.0000 | 2.70 | 0.924 | -2.13 dB | 0 | 1 |
| **amrwb_optimized_psychoacoustic_spectral_shaping** | 1 | 1.0000 | 1.0000 | 2.84 | 0.923 | -2.00 dB | 0 | 1 |
| **AMRWB_Opus_Robust_Spectral_Phase_Exploit** | 1 | 0.7500 | 0.7500 | 3.17 | 0.850 | -2.21 dB | 0 | 1 |
| **amrwb_freq_phase_masked_attack** | 1 | 0.6667 | 0.6667 | 1.77 | 0.643 | -3.20 dB | 0 | 1 |
| **amrwb_opus_freq_phase_adv** | 1 | 0.6000 | 0.6000 | 2.17 | 0.743 | -3.07 dB | 0 | 1 |
| **amrwb_psychoacoustic_frequency_masking_phase_jitter** | 1 | 0.6000 | 0.6000 | 2.68 | 0.918 | -1.89 dB | 0 | 1 |
| **amrwb_opus_freq_phase_robust** | 2 | 0.5000 | 1.0000 | 2.54 | 0.909 | -2.80 dB | 0 | 1 |
| **amrwb_opus_spectral_phase_masking** | 1 | 0.4444 | 0.4444 | 3.23 | 0.907 | -3.53 dB | 0 | 1 |
| **amrwb_opus_frequency_domain_psychoacoustic_shift** | 1 | 0.4286 | 0.4286 | 3.35 | 0.887 | -2.01 dB | 0 | 1 |
| **amrwb_opus_spectral_phase_advancement** | 1 | 0.4286 | 0.4286 | 3.29 | 0.884 | -1.94 dB | 0 | 1 |

## Quality Metrics Distribution

### PESQ Distribution

| Quality Level | Range | Count | Percentage |
|---------------|-------|-------|------------|
| Excellent | 4.0+ | 0 | 0.0% |
| Good | 3.5+ to 4.0 | 16 | 10.8% |
| Fair | 3.0+ to 3.5 | 67 | 45.3% |
| Poor | 2.0+ to 3.0 | 55 | 37.2% |
| Bad | 0+ to 2.0 | 10 | 6.8% |

### STOI Distribution

| Quality Level | Range | Count | Percentage |
|---------------|-------|-------|------------|
| Excellent | 0.99 to 1.00 | 0 | 0.0% |
| Very Good | 0.95 to 0.99 | 0 | 0.0% |
| Good | 0.85 to 0.95 | 107 | 72.3% |
| Fair | 0.75 to 0.85 | 33 | 22.3% |
| Poor | 0.00 to 0.75 | 8 | 5.4% |

### SNR Distribution

| Quality Level | Range | Count | Percentage |
|---------------|-------|-------|------------|
| Excellent | ≥ 30 dB | 0 | 0.0% |
| Good | 20 to 30 dB | 0 | 0.0% |
| Acceptable | 10 to 20 dB | 0 | 0.0% |
| Poor | 0 to 10 dB | 4 | 2.7% |
| Very Poor (Negative) | < 0 dB | 144 | 97.3% |

## Conclusions

### 1. Constraint Compliance Failure

- **0% of iterations meet all quality constraints** (PESQ ≥ 3.5, STOI ≥ 0.85, SNR ≥ 20.0 dB)
- This is consistent with the AMR-WB analysis showing that the codec is too lossy for strict quality requirements
- Primary failure mode: **SNR is negative** (compression artifacts louder than signal)

### 2. Attack Effectiveness

- **57.4% attack success rate** (WER > 0)
- Mean WER for successful attacks: 0.2910
- AMR-WB shows higher attack effectiveness than OPUS, but at severe quality cost

### 3. Quality Metrics

- **Mean PESQ: 2.95** (below 3.5 threshold)
- **Mean STOI: 0.872** (mostly above 0.85 threshold)
- **Mean SNR: -2.54 dB** (negative - artifacts dominate signal)

### 4. Category Performance

- **long-signals**: 64.0% attack success, 0.0% constraint compliance
- **medium-signals**: 75.0% attack success, 0.0% constraint compliance
- **short-signals**: 34.0% attack success, 0.0% constraint compliance

### 5. Strategy Diversity

- **125 unique strategies** tested across 148 iterations
- High strategy diversity suggests extensive exploration of perturbation space
- Top strategies show varying effectiveness, with some achieving higher WER deltas

---

**Note:** All results are for AMR-WB codec only. The zero constraint compliance rate confirms that AMR-WB compression introduces artifacts too severe to meet strict quality thresholds, even when perturbations themselves may be imperceptible before compression.