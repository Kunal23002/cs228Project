# AMR-WB Codec Issue Analysis

## Problem Summary
AMR-WB codec encoding/decoding is **working correctly**, but **all iterations fail to meet quality constraints** after compression. This is why no AMR-WB results appear in the batch results JSON file.

## Root Cause

### The Issue: Compression Artifacts Exceed Quality Thresholds

AMR-WB is a **very lossy codec** designed for low bitrates (6.6-23.85 kbps). When perturbed audio is compressed through AMR-WB, the compression artifacts combined with the perturbation cause metrics to fall below required thresholds.

### Evidence from Notebook Output

Example AMR-WB metrics from the notebook:
```
Step 8: Computing metrics on compressed audio...
  WER: 0.000 (Δ: +0.000)
  CER: 0.000 (Δ: +0.000)
  PESQ: 3.00        ❌ (Required: ≥ 3.5)
  STOI: 0.840       ❌ (Required: ≥ 0.85)
  SNR: -3.17 dB     ❌ (Required: ≥ 20.0 dB)
```

**Key Problems:**
1. **PESQ < 3.5**: Audio quality degraded below "good" threshold
2. **STOI < 0.85**: Speech intelligibility reduced
3. **SNR is NEGATIVE**: Compression artifacts are LOUDER than the signal itself!

### Why This Happens

1. **AMR-WB is inherently lossy**: Designed for telephony (low bitrates), it introduces significant compression artifacts
2. **Perturbation + Compression = Double degradation**: 
   - Perturbation adds noise
   - AMR-WB compression adds artifacts
   - Combined effect exceeds quality thresholds
3. **SNR calculation**: When comparing original vs compressed audio, the compression artifacts are so severe that they dominate, resulting in negative SNR

## Technical Details

### Quality Constraints (from code):
```python
MIN_PESQ = 3.5    # Minimum PESQ score (3.5+ = "good" quality)
MIN_STOI = 0.85   # Minimum STOI score (0.85+ = highly intelligible)
MIN_SNR = 20.0    # Minimum SNR in dB (perturbation must be 20dB below signal)
```

### AMR-WB Configuration:
```python
"amr-wb": {
    "codec": "libvo_amrwbenc", 
    "bitrates": [6.6, 8.85, 12.65, 14.25, 15.85, 18.25, 19.85, 23.05, 23.85]
}
```

### Encoding Process:
1. Perturbed audio is created (meets constraints before compression)
2. Audio is encoded to AMR-WB at low bitrate (6.6-23.85 kbps)
3. Audio is decoded back to WAV
4. **Metrics are computed on the compressed audio** (not the perturbed audio)
5. Compressed audio fails quality constraints

## Why OPUS Works But AMR-WB Doesn't

| Codec | Bitrate Range | Compression Quality | Result |
|-------|---------------|---------------------|--------|
| **OPUS** | 32-128 kbps | High quality, less lossy | ✅ Meets constraints |
| **AMR-WB** | 6.6-23.85 kbps | Very lossy, telephony-grade | ❌ Fails constraints |

**OPUS** operates at much higher bitrates (32-128 kbps) and uses modern compression algorithms, resulting in minimal quality degradation.

**AMR-WB** operates at very low bitrates (6.6-23.85 kbps) and is optimized for speech telephony, introducing significant artifacts that degrade quality metrics.

## Solutions

### Option 1: Relax Constraints for AMR-WB (Recommended)
Modify the constraint checking to use different thresholds for AMR-WB:

```python
def find_best_iteration_per_codec(self, results, ...):
    # Use relaxed constraints for AMR-WB
    for codec, codec_results in results_by_codec.items():
        if codec == "amr-wb":
            min_pesq = 2.5  # Lower threshold for AMR-WB
            min_stoi = 0.75  # Lower threshold for AMR-WB
            min_snr = 10.0   # Lower threshold for AMR-WB
        else:
            min_pesq = MIN_PESQ
            min_stoi = MIN_STOI
            min_snr = MIN_SNR
```

### Option 2: Compute Metrics on Pre-Compression Audio
Instead of computing metrics on compressed audio, compute them on the perturbed audio before compression. However, this defeats the purpose of testing codec robustness.

### Option 3: Use Higher AMR-WB Bitrates Only
Restrict AMR-WB to only the highest bitrates (19.85, 23.05, 23.85 kbps) which may produce better quality.

### Option 4: Separate Quality Assessment
Compute quality metrics on perturbed audio (pre-compression) but still test ASR on compressed audio. This separates perturbation quality from compression quality.

## Current Behavior

The code correctly:
1. ✅ Encodes to AMR-WB successfully
2. ✅ Decodes from AMR-WB successfully  
3. ✅ Computes metrics on compressed audio
4. ✅ Filters out results that don't meet constraints
5. ✅ Reports "⚠️ No AMR-WB iteration met constraints"

**The system is working as designed** - it's just that AMR-WB compression is too lossy to meet the strict quality requirements when combined with perturbations.

## Recommendation

**Implement Option 1**: Use codec-specific quality thresholds. AMR-WB is inherently more lossy, so it's reasonable to have different quality expectations. This would allow AMR-WB results to be included in the batch results while still maintaining quality standards appropriate for that codec.

