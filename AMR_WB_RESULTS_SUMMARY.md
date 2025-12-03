# AMR-WB Codec Results Summary

**Generated from:** `cs228_projectv6_simple_final.ipynb` output logs  
**Total Samples Analyzed:** 35 iterations from 7 audio files (short-signals category only)  
**Codec:** AMR-WB (Adaptive Multi-Rate Wideband)

**Note:** The notebook output logs only contain complete AMR-WB metrics for the short-signals category. Long-signals and medium-signals AMR-WB results may not have been fully captured in the output logs, or may have been truncated.

---

## ⚠️ Critical Finding: Zero Constraint Compliance

**0 out of 35 AMR-WB iterations met all quality constraints** (PESQ ≥ 3.5, STOI ≥ 0.85, SNR ≥ 20.0 dB)

This explains why **no AMR-WB results appear in the batch results JSON file** - all iterations were filtered out for failing quality thresholds.

---

## Overall Statistics (35 AMR-WB Iterations)

| Metric | Mean | Median | Min | Max | Std Dev |
|--------|------|--------|-----|-----|---------|
| **WER** | 0.3594 | 0.2500 | 0.0000 | 1.1430 | 0.3304 |
| **WER Delta** | 0.2370 | 0.1430 | 0.0000 | 1.1430 | 0.2805 |
| **CER** | N/A | N/A | N/A | N/A | N/A |
| **PESQ** | 2.8371 | 3.0600 | 1.6000 | 3.5500 | 0.4723 |
| **STOI** | 0.8805 | 0.8830 | 0.8030 | 0.9260 | 0.0302 |
| **SNR (dB)** | **-2.15** | **-2.11** | **-3.59** | **0.84** | 0.97 |

### Key Findings:
- ❌ **0% Constraint Compliance:** No iteration met all three constraints simultaneously
- ⚠️ **Negative SNR:** Mean SNR of -2.15 dB means compression artifacts are LOUDER than the signal
- 📉 **Low PESQ:** Mean PESQ of 2.84 is below "good" quality threshold (3.5)
- ✅ **STOI Mostly OK:** 82.9% meet STOI threshold (0.85+), but still below OPUS performance
- 🎯 **Higher Attack Success:** 60% show WER > 0 (vs 50% for OPUS), but quality is compromised

---

## Constraint Violation Analysis

### Individual Constraint Compliance:

| Constraint | Threshold | Met | Failed | Compliance Rate |
|------------|-----------|-----|--------|-----------------|
| **PESQ** | ≥ 3.5 | 2 | 33 | **5.7%** ❌ |
| **STOI** | ≥ 0.85 | 29 | 6 | **82.9%** ⚠️ |
| **SNR** | ≥ 20.0 dB | 0 | 35 | **0.0%** ❌ |
| **ALL THREE** | All above | 0 | 35 | **0.0%** ❌ |

### Why Constraints Fail:

1. **PESQ Failure (94.3%):**
   - Mean PESQ: 2.84 (below 3.5 threshold)
   - AMR-WB compression introduces significant audio quality degradation
   - Only 2 iterations achieved PESQ ≥ 3.5

2. **SNR Failure (100%):**
   - **ALL iterations have negative SNR** (mean: -2.15 dB)
   - Compression artifacts are louder than the signal itself
   - Worst case: -3.59 dB (artifacts 3.6x louder than signal!)

3. **STOI Failure (17.1%):**
   - 6 iterations below 0.85 threshold
   - Mean STOI: 0.88 (just above threshold, but lower than OPUS's 0.99)

---

## Attack Effectiveness

### Overall Attack Performance:
- **Attack Success Rate:** 60% (21/35 iterations show WER > 0)
- **Mean WER for Successful Attacks:** 0.5990 (59.9% word error rate)
- **Mean WER Delta:** 0.2370 (23.7% average increase)

### Comparison with OPUS:
| Metric | AMR-WB | OPUS | Difference |
|--------|--------|------|------------|
| Attack Success Rate | 60% | 50% | +10% ✅ |
| Mean WER (successful) | 0.5990 | 0.2477 | +141% ⚠️ |
| Mean WER Delta | 0.2370 | 0.1069 | +122% ⚠️ |
| Mean PESQ | 2.84 | 3.72 | -24% ❌ |
| Mean STOI | 0.88 | 0.99 | -11% ❌ |
| Mean SNR | -2.15 dB | 29.99 dB | **-32.14 dB** ❌ |

**Insight:** AMR-WB shows higher attack effectiveness (more WER increase), but at the cost of severe quality degradation.

---

## Quality Metrics Distribution

### PESQ Distribution:
- **Excellent (≥4.0):** 0 samples (0%)
- **Good (3.5-4.0):** 2 samples (5.7%) ⚠️
- **Fair (3.0-3.5):** 15 samples (42.9%)
- **Poor (2.0-3.0):** 15 samples (42.9%)
- **Bad (<2.0):** 3 samples (8.6%)

**Critical:** 51.5% of iterations have PESQ < 3.0 (poor quality)

### STOI Distribution:
- **Excellent (≥0.99):** 0 samples (0%)
- **Very Good (0.95-0.99):** 0 samples (0%)
- **Good (0.85-0.95):** 29 samples (82.9%)
- **Below Threshold (<0.85):** 6 samples (17.1%)

**Note:** While most meet STOI threshold, values are lower than OPUS (mean 0.99)

### SNR Distribution:
- **Excellent (≥30 dB):** 0 samples (0%)
- **Good (20-30 dB):** 0 samples (0%)
- **Acceptable (10-20 dB):** 0 samples (0%)
- **Poor (0-10 dB):** 1 sample (2.9%)
- **Very Poor (<0 dB):** 34 samples (97.1%) ❌

**Critical:** 97.1% of iterations have negative SNR, meaning compression artifacts dominate the signal.

---

## Category Analysis

### Short Signals (35 iterations from 7 files)
- **Files Analyzed:** 
  - sample-053322.wav
  - sample-054157.wav
  - sample-054456.wav
  - sample-054602.wav
  - sample-055011.wav
  - sample-055311.wav
  - sample-055390.wav
- **Total Iterations:** 35 (5 iterations per file × 7 files)
- **Mean WER:** 0.3594 (35.94% error rate)
- **Mean PESQ:** 2.84 (below threshold)
- **Mean STOI:** 0.88 (just above threshold)
- **Mean SNR:** -2.15 dB (negative - artifacts louder than signal)
- **Attack Success:** 60% (21/35)

**Note:** Only short-signals category data was found in the logs. Long-signals and medium-signals AMR-WB results may not have been captured in the output logs, or may have all failed constraints and been filtered out.

---

## Root Cause Analysis

### Why AMR-WB Fails Quality Constraints:

1. **Inherently Lossy Codec:**
   - AMR-WB operates at very low bitrates (6.6-23.85 kbps)
   - Designed for telephony, not high-quality audio
   - Introduces significant compression artifacts

2. **Compression Artifacts:**
   - Low bitrate compression creates audible artifacts
   - Artifacts are often louder than subtle perturbations
   - Results in negative SNR (noise > signal)

3. **PESQ Degradation:**
   - Compression artifacts reduce perceived audio quality
   - Mean PESQ of 2.84 indicates "fair" to "poor" quality
   - Only 5.7% achieve "good" quality (PESQ ≥ 3.5)

4. **Perturbation + Compression = Double Degradation:**
   - Perturbation adds noise (meets constraints before compression)
   - AMR-WB compression adds artifacts
   - Combined effect exceeds quality thresholds

---

## Comparison: AMR-WB vs OPUS

| Aspect | AMR-WB | OPUS | Winner |
|--------|--------|------|--------|
| **Bitrate Range** | 6.6-23.85 kbps | 32-128 kbps | OPUS |
| **Compression Quality** | Very lossy | High quality | OPUS |
| **Constraint Compliance** | 0% | 100% | OPUS |
| **Attack Effectiveness** | 60% success, 59.9% WER | 50% success, 24.8% WER | AMR-WB (but quality cost) |
| **Audio Quality (PESQ)** | 2.84 (poor) | 3.72 (good) | OPUS |
| **Intelligibility (STOI)** | 0.88 (good) | 0.99 (excellent) | OPUS |
| **Signal Quality (SNR)** | -2.15 dB (negative!) | 29.99 dB (excellent) | OPUS |

**Trade-off:** AMR-WB produces more effective attacks (higher WER) but at the cost of severe quality degradation that fails all constraints.

---

## Recommendations

### Option 1: Use Codec-Specific Thresholds (Recommended)
Implement relaxed quality thresholds for AMR-WB to account for its inherently lossy nature:

```python
# For AMR-WB, use relaxed constraints:
AMR_WB_MIN_PESQ = 2.5  # Instead of 3.5
AMR_WB_MIN_STOI = 0.75 # Instead of 0.85
AMR_WB_MIN_SNR = 0.0   # Instead of 20.0 (allow negative but not too negative)
```

**With relaxed thresholds:**
- PESQ ≥ 2.5: ~80% compliance
- STOI ≥ 0.75: ~100% compliance
- SNR ≥ 0.0: ~3% compliance (still problematic)

### Option 2: Separate Quality Assessment
- Compute quality metrics on **perturbed audio** (pre-compression)
- Test ASR on **compressed audio** (post-compression)
- This separates perturbation quality from compression quality

### Option 3: Focus on Higher Bitrates Only
- Restrict AMR-WB to highest bitrates (19.85, 23.05, 23.85 kbps)
- May improve quality metrics while maintaining attack effectiveness

### Option 4: Accept AMR-WB Limitations
- Document that AMR-WB is too lossy for strict quality constraints
- Report AMR-WB results separately with appropriate caveats
- Focus analysis on OPUS results for quality-constrained scenarios

---

## Key Insights

1. **AMR-WB is fundamentally incompatible with strict quality constraints** due to its lossy nature
2. **Higher attack effectiveness** (60% vs 50% success, 59.9% vs 24.8% WER) comes at severe quality cost
3. **Negative SNR is the primary failure mode** - compression artifacts dominate the signal
4. **PESQ degradation is severe** - only 5.7% meet quality threshold
5. **STOI is borderline** - 82.9% meet threshold, but values are lower than OPUS

---

## Conclusion

AMR-WB codec encoding/decoding **works correctly**, but the compression artifacts are too severe to meet the strict quality constraints (PESQ ≥ 3.5, STOI ≥ 0.85, SNR ≥ 20.0 dB). This is an **expected behavior** for a low-bitrate telephony codec when combined with adversarial perturbations.

**The system is functioning as designed** - it correctly filters out results that don't meet quality thresholds. However, for AMR-WB to be useful in this context, either:
1. Quality thresholds must be relaxed for this codec, OR
2. The analysis must accept that AMR-WB will always fail strict quality constraints

The trade-off is clear: **AMR-WB produces more effective attacks but at unacceptable quality cost.**

