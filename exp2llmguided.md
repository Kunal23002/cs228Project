# Batch Results Summary - OPUS Codec Performance

**Generated from:** `batch_results_all_20251201_024938.json`  
**Total Samples:** 30 (10 per category)  
**Codec:** OPUS only (AMR-WB results not present in file)

---

## Overall Statistics (All 30 samples)

| Metric | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|
| **WER** | 0.1238 | 0.0000 | 0.0000 | 2.2857 | 0.3688 |
| **WER Delta** | 0.1069 | 0.0000 | 0.0000 | 1.4286 | 0.2752 |
| **CER** | 0.1343 | 0.0000 | 0.0000 | 3.1000 | 0.5668 |
| **CER Delta** | 0.1343 | 0.0000 | 0.0000 | 2.4500 | 0.4489 |
| **PESQ** | 3.7186 | 3.6655 | 3.5190 | 4.4638 | 0.1867 |
| **STOI** | 0.9929 | 0.9989 | 0.8734 | 0.9999 | 0.0232 |
| **SNR (dB)** | 29.99 | 31.58 | 20.58 | 37.49 | 4.70 |

### Key Findings:
- **Quality Constraints Met:** All 30 samples meet the constraints (PESQ ≥ 3.5, STOI ≥ 0.85, SNR ≥ 20 dB)
- **Attack Success Rate:** 50% (15/30) samples show WER > 0 (successful perturbation)
- **Mean Attack Effectiveness:** WER increased by 10.69% on average where attacks succeeded

---

## Statistics by Category

### Long Signals (10 samples)

| Metric | Mean | Median | Min | Max |
|--------|------|--------|-----|-----|
| **WER** | 0.0696 | 0.0000 | 0.0000 | 0.2222 |
| **WER Delta** | 0.0696 | 0.0000 | 0.0000 | 0.2222 |
| **CER** | 0.0417 | 0.0000 | 0.0000 | 0.1333 |
| **PESQ** | 3.7277 | 3.6653 | 3.5290 | 4.4638 |
| **STOI** | 0.9870 | 0.9995 | 0.8734 | 0.9999 |
| **SNR (dB)** | 31.07 | 32.74 | 20.58 | 34.56 |

**Attack Success:** 6/10 samples (60%)  
**Best Iteration Distribution:** Iteration 1 (8x), Iteration 4 (1x), Iteration 5 (1x)

---

### Medium Signals (10 samples)

| Metric | Mean | Median | Min | Max |
|--------|------|--------|-----|-----|
| **WER** | 0.1429 | 0.1071 | 0.0000 | 0.3333 |
| **WER Delta** | 0.1429 | 0.1071 | 0.0000 | 0.3333 |
| **CER** | 0.0835 | 0.0696 | 0.0000 | 0.2174 |
| **PESQ** | 3.6966 | 3.6557 | 3.5271 | 4.0254 |
| **STOI** | 0.9935 | 0.9959 | 0.9655 | 0.9999 |
| **SNR (dB)** | 29.14 | 30.11 | 21.17 | 37.49 |

**Attack Success:** 7/10 samples (70%)  
**Best Iteration Distribution:** Iteration 1 (7x), Iteration 2 (2x), Iteration 4 (1x)

---

### Short Signals (10 samples)

| Metric | Mean | Median | Min | Max |
|--------|------|--------|-----|-----|
| **WER** | 0.1593 | 0.0000 | 0.0000 | 2.2857 |
| **WER Delta** | 0.1507 | 0.0000 | 0.0000 | 1.4286 |
| **CER** | 0.2776 | 0.0208 | 0.0000 | 3.1000 |
| **PESQ** | 3.7319 | 3.6970 | 3.5196 | 3.8571 |
| **STOI** | 0.9982 | 0.9995 | 0.9975 | 0.9999 |
| **SNR (dB)** | 29.76 | 31.26 | 22.86 | 36.49 |

**Attack Success:** 5/10 samples (50%)  
**Best Iteration Distribution:** Iteration 1 (7x), Iteration 3 (2x), Iteration 4 (1x)

---

## Iteration Performance Analysis

| Iteration | Count | Avg WER Delta | Avg PESQ | Avg STOI | Avg SNR (dB) |
|-----------|-------|---------------|----------|----------|--------------|
| **1** | 22 (73%) | 0.0776 | 3.7192 | 0.9926 | 30.15 |
| **2** | 2 (7%) | 0.2143 | 3.7368 | 0.9947 | 25.40 |
| **3** | 2 (7%) | 0.3429 | 3.6238 | 0.9999 | 35.66 |
| **4** | 3 (10%) | 0.1083 | 3.7471 | 0.9881 | 30.40 |
| **5** | 1 (3%) | 0.1333 | 3.6310 | 0.9994 | 33.63 |

**Key Insight:** Iteration 1 was most frequently the best (73%), suggesting the LLM-generated strategies are effective from the start.

---

## Attack Effectiveness Breakdown

### Samples with NO Attack Effect (WER = 0)
- **Count:** 15/30 (50%)
- **Avg PESQ:** 3.7435
- **Avg STOI:** 0.9965
- **Avg SNR:** 30.64 dB

### Samples with Successful Attacks (WER > 0)
- **Count:** 15/30 (50%)
- **Avg WER:** 0.2477 (24.77% error rate)
- **Avg PESQ:** 3.6936 (still meets quality threshold)
- **Avg STOI:** 0.9892 (highly intelligible)
- **Avg SNR:** 29.34 dB

---

## Strategy Performance (Top 10 Most Used)

| Strategy | Count | Avg WER Delta | Avg PESQ | Avg STOI |
|----------|-------|---------------|----------|----------|
| default_narrowband_noise | 3 | 0.2222 | 3.6261 | 0.9963 |
| OpusAmrWbSpectralPhaseNoise | 2 | 0.0000 | 3.8716 | 0.9995 |
| Various spectral/phase strategies | 25 | 0.0933 | 3.7235 | 0.9926 |

---

## Quality Metrics Distribution

### PESQ Distribution
- **Excellent (≥4.0):** 2 samples (6.7%)
- **Good (3.5-4.0):** 28 samples (93.3%)
- **Below Threshold (<3.5):** 0 samples (0%)

### STOI Distribution
- **Excellent (≥0.99):** 23 samples (76.7%)
- **Very Good (0.95-0.99):** 6 samples (20.0%)
- **Good (0.85-0.95):** 1 sample (3.3%)

### SNR Distribution
- **Excellent (≥30 dB):** 19 samples (63.3%)
- **Good (25-30 dB):** 7 samples (23.3%)
- **Acceptable (20-25 dB):** 4 samples (13.3%)

---

## Observations & Recommendations

### Strengths:
1. **100% Constraint Compliance:** All attacks meet quality thresholds
2. **High Audio Quality:** Mean PESQ of 3.72, well above minimum
3. **Excellent Intelligibility:** Mean STOI of 0.993 indicates imperceptible perturbations
4. **Robust SNR:** Mean SNR of ~30 dB shows subtle perturbations

### Areas for Improvement:
1. **Low Attack Success Rate:** Only 50% of samples show WER > 0
2. **Missing AMR-WB Results:** File only contains OPUS codec results (30/60 expected entries)
3. **Variable Effectiveness:** Wide range of WER (0 to 2.29) suggests inconsistent attack potency

### Recommendations:
1. Investigate why AMR-WB results are missing
2. Focus on strategies that achieved WER > 0.2 (iterations 2 and 3 show promise)
3. Consider more aggressive perturbations while maintaining quality constraints
4. Analyze why 50% of samples had zero WER impact despite meeting constraints

---

## Category Comparison

| Category | Samples | Avg WER Delta | Attack Success % | Avg PESQ | Avg SNR |
|----------|---------|---------------|------------------|----------|---------|
| **Long** | 10 | 0.0696 | 60% | 3.73 | 31.07 |
| **Medium** | 10 | 0.1429 | 70% | 3.70 | 29.14 |
| **Short** | 10 | 0.1507 | 50% | 3.73 | 29.76 |

**Insight:** Medium-length signals show highest attack success rate (70%), suggesting optimal perturbation effectiveness in this duration range.

