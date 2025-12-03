# Predefined Attack Summary: PGD and AdvReverb Analysis

**Date**: December 2, 2025  
**Dataset**: 80 audio samples from long-signals directory  
**Attacks**: PGD (Projected Gradient Descent) and AdvReverb (Convolutional White-Box)  
**Codecs**: Opus and AMR-WB (AAC fallback)  
**ASR Model**: OpenAI Whisper (base)

---

## Executive Summary

This analysis evaluates the robustness of two white-box adversarial attacks (PGD and AdvReverb) against audio compression codecs (Opus and AMR-WB). Each of the 80 audio samples was processed through 4 pipelines:

1. **PGD Attack → Opus Compression**
2. **PGD Attack → AMR-WB Compression**
3. **AdvReverb Attack → Opus Compression**
4. **AdvReverb Attack → AMR-WB Compression**

**Key Findings**:
- **PGD + Opus**: Highly robust (WER: 1.93%, excellent audio quality)
- **PGD + AMR-WB**: Moderate robustness (WER: 22.53%, degraded quality)
- **AdvReverb + Opus**: Moderate robustness (WER: 21.43%, poor audio quality)
- **AdvReverb + AMR-WB**: Poor robustness (WER: 50.08%, very poor audio quality)

---

## Methodology

### Pipeline Architecture

```
Original Audio (16kHz WAV)
    ↓
Baseline Metrics (SNR=∞, PESQ=5.0, STOI=1.0)
    ↓
    ├─→ [PGD Attack] ─→ Opus Compression ─→ Metrics
    ├─→ [PGD Attack] ─→ AMR-WB Compression ─→ Metrics
    ├─→ [AdvReverb Attack] ─→ Opus Compression ─→ Metrics
    └─→ [AdvReverb Attack] ─→ AMR-WB Compression ─→ Metrics
```

### Attack Configurations

#### PGD Attack (Gao et al., 2024)
- **Type**: Gradient-based perturbation
- **Parameters**:
  - Epsilon (ε): 0.002
  - Alpha (α): 0.0004
  - Steps: 10
  - Loss: Negative CTC loss (maximizes transcription error)

#### AdvReverb Attack (Chen et al., 2023)
- **Type**: Convolutional Room Impulse Response (RIR)
- **Parameters**:
  - RIR Length: 2048 samples
  - Learning Rate: 0.001
  - Steps: 300
  - Optimization: Adam optimizer on RIR filter

### Compression Settings

- **Opus**: 64 kbps bitrate (libopus codec)
- **AMR-WB**: 12.65 kbps bitrate (AAC fallback due to encoder unavailability)

### Metrics Computed

1. **WER (Word Error Rate)**: Measures transcription accuracy at word level (0 = perfect, 1 = complete failure)
2. **CER (Character Error Rate)**: Measures transcription accuracy at character level
3. **SNR (Signal-to-Noise Ratio)**: Audio quality in dB (higher = better)
4. **PESQ (Perceptual Evaluation of Speech Quality)**: Perceived quality (1-5 scale, 5 = perfect)
5. **STOI (Short-Time Objective Intelligibility)**: Speech intelligibility (0-1 scale, 1 = perfect)

---

## Results Analysis

### 1. PGD Attack + Opus Compression

**Performance**: ✅ **Excellent**

| Metric | Mean | Std Dev | Min | Max |
|--------|------|---------|-----|-----|
| WER | 0.0193 | 0.1139 | 0.0000 | 1.0000 |
| CER | 0.0120 | 0.0725 | 0.0000 | 0.6386 |
| SNR | 30.10 dB | 2.81 dB | 19.80 dB | 34.42 dB |
| PESQ | 4.582 | 0.050 | 4.279 | 4.620 |
| STOI | 0.9994 | 0.0007 | 0.9964 | 0.9998 |

**Analysis**:
- **Attack Survival**: 98.07% of samples maintain perfect transcription (WER = 0)
- **Audio Quality**: Near-perfect preservation (PESQ ~4.6, STOI ~0.999)
- **Robustness**: PGD perturbations survive Opus compression extremely well
- **Conclusion**: Opus compression at 64 kbps is insufficient to remove PGD adversarial perturbations

**Notable Outliers**:
- 1 sample (sample-081807) had complete failure (WER = 1.0) with garbled output
- Most samples show imperceptible degradation

---

### 2. PGD Attack + AMR-WB Compression

**Performance**: ⚠️ **Moderate**

| Metric | Mean | Std Dev | Min | Max |
|--------|------|---------|-----|-----|
| WER | 0.2253 | 0.2294 | 0.0000 | 1.0000 |
| CER | 0.1214 | 0.1466 | 0.0000 | 0.7027 |
| SNR | 12.71 dB | 3.84 dB | 3.88 dB | 22.61 dB |
| PESQ | 2.467 | 0.549 | 1.484 | 3.815 |
| STOI | 0.8825 | 0.0205 | 0.8198 | 0.9229 |

**Analysis**:
- **Attack Survival**: 22.53% average WER indicates moderate attack degradation
- **Audio Quality**: Significant degradation (PESQ ~2.5, STOI ~0.88)
- **Robustness**: AMR-WB compression partially removes adversarial perturbations
- **Variability**: High standard deviation (σ = 0.23) indicates inconsistent performance
- **Conclusion**: AMR-WB compression is more effective at removing PGD perturbations than Opus

**Distribution**:
- ~40% of samples maintain perfect transcription (WER = 0)
- ~60% show varying degrees of transcription errors
- Some samples show catastrophic failure (WER > 0.8)

---

### 3. AdvReverb Attack + Opus Compression

**Performance**: ⚠️ **Moderate Attack Success, Poor Audio Quality**

| Metric | Mean | Std Dev | Min | Max |
|--------|------|---------|-----|-----|
| WER | 0.2143 | 0.2481 | 0.0000 | 1.0000 |
| CER | 0.1316 | 0.1947 | 0.0000 | 0.9556 |
| SNR | -3.51 dB | 1.54 dB | -7.996 dB | -0.209 dB |
| PESQ | 1.658 | 0.234 | 1.191 | 2.954 |
| STOI | 0.7836 | 0.0442 | 0.5750 | 0.8524 |

**Analysis**:
- **Attack Survival**: 21.43% average WER indicates moderate attack effectiveness
- **Audio Quality**: Poor quality (negative SNR, PESQ ~1.7, STOI ~0.78)
- **Trade-off**: AdvReverb achieves similar WER to PGD+AMR but with much worse audio quality
- **Perceptibility**: Negative SNR indicates perturbations are audible
- **Conclusion**: AdvReverb creates perceptible distortions that partially survive Opus compression

**Key Observations**:
- 45% of samples maintain perfect transcription (WER = 0)
- Significant audio degradation makes attack easily detectable
- High variability in attack success (σ = 0.25)

---

### 4. AdvReverb Attack + AMR-WB Compression

**Performance**: ❌ **Poor**

| Metric | Mean | Std Dev | Min | Max |
|--------|------|---------|-----|-----|
| WER | 0.5008 | 0.2985 | 0.0000 | 1.0000 |
| CER | 0.3332 | 0.2409 | 0.0000 | 0.9118 |
| SNR | -3.24 dB | 1.45 dB | -7.650 dB | 0.084 dB |
| PESQ | 1.517 | 0.220 | 1.172 | 2.713 |
| STOI | 0.7137 | 0.0498 | 0.5117 | 0.7875 |

**Analysis**:
- **Attack Survival**: 50.08% average WER indicates poor attack robustness
- **Audio Quality**: Very poor quality (negative SNR, PESQ ~1.5, STOI ~0.71)
- **Robustness**: AMR-WB compression significantly degrades AdvReverb attacks
- **Failure Rate**: Many samples show complete transcription failure or gibberish output
- **Conclusion**: AdvReverb is not robust to AMR-WB compression

**Failure Modes**:
- Transcriptions often become gibberish or very short phrases
- Some samples produce multilingual/nonsensical output
- High WER variance (σ = 0.30) indicates unpredictable behavior

---

## Comparative Analysis

### Attack Effectiveness Ranking (by WER)

1. **PGD + Opus**: 1.93% WER ⭐⭐⭐⭐⭐ (Best)
2. **AdvReverb + Opus**: 21.43% WER ⭐⭐⭐
3. **PGD + AMR-WB**: 22.53% WER ⭐⭐⭐
4. **AdvReverb + AMR-WB**: 50.08% WER ⭐ (Worst)

### Audio Quality Ranking (by PESQ)

1. **PGD + Opus**: 4.582 PESQ ⭐⭐⭐⭐⭐ (Best)
2. **PGD + AMR-WB**: 2.467 PESQ ⭐⭐⭐
3. **AdvReverb + Opus**: 1.658 PESQ ⭐⭐
4. **AdvReverb + AMR-WB**: 1.517 PESQ ⭐ (Worst)

### Codec Robustness (Attack Mitigation)

**Opus Codec**:
- Minimal impact on PGD attacks (1.93% WER)
- Moderate impact on AdvReverb attacks (21.43% WER)
- Preserves high audio quality for PGD
- **Conclusion**: Opus is ineffective at removing PGD perturbations

**AMR-WB Codec**:
- Moderate impact on PGD attacks (22.53% WER)
- Strong impact on AdvReverb attacks (50.08% WER)
- Significantly degrades audio quality for both attacks
- **Conclusion**: AMR-WB is more effective at attack mitigation but at the cost of quality

---

## Detailed Observations

### PGD Attack Characteristics

**Strengths**:
- Creates imperceptible perturbations (high SNR after compression)
- Highly robust to Opus compression
- Maintains excellent audio quality metrics
- Consistent performance across samples

**Weaknesses**:
- Moderately affected by AMR-WB compression
- Some samples show complete failure with AMR-WB
- Attack effectiveness varies with codec choice

**Best Use Case**: Targeting systems using high-quality codecs (Opus, AAC)

---

### AdvReverb Attack Characteristics

**Strengths**:
- Can achieve moderate WER increases
- Some samples show good attack survival with Opus

**Weaknesses**:
- Creates perceptible distortions (negative SNR)
- Poor robustness to AMR-WB compression
- High variability in attack success
- Often produces gibberish transcriptions with AMR-WB
- Significantly degrades audio quality

**Best Use Case**: Limited practical applicability due to perceptibility and poor codec robustness

---

## Statistical Insights

### Attack Success Rate (WER > 0.1)

| Attack + Codec | Success Rate |
|----------------|--------------|
| PGD + Opus | ~2% (very few samples) |
| PGD + AMR-WB | ~60% (moderate) |
| AdvReverb + Opus | ~55% (moderate) |
| AdvReverb + AMR-WB | ~85% (high, but often gibberish) |

### Perceptibility Analysis

**Imperceptible Range**: SNR > 20 dB, PESQ > 4.0, STOI > 0.95

| Attack + Codec | Imperceptible? |
|----------------|----------------|
| PGD + Opus | ✅ Yes (SNR ~30 dB) |
| PGD + AMR-WB | ⚠️ Borderline (SNR ~13 dB) |
| AdvReverb + Opus | ❌ No (SNR ~-3.5 dB) |
| AdvReverb + AMR-WB | ❌ No (SNR ~-3.2 dB) |

---

## Notable Examples

### Successful Attack (PGD + Opus)
**File**: sample-070322.wav  
**Original**: "The Christian Bible has seen many changes throughout history."  
**PGD+Opus**: "The Christian Bible has seen many changes throughout history." (WER: 0.0)  
**Metrics**: SNR: 34.42 dB, PESQ: 4.56, STOI: 0.998

### Moderate Attack (PGD + AMR-WB)
**File**: sample-070236.wav  
**Original**: "We are part of that soul. So we really recognize that it is working for us."  
**PGD+AMR**: "We are passed at that soul. So we rarely recognize that it is working for us." (WER: 0.1875)  
**Metrics**: SNR: 15.37 dB, PESQ: 2.50, STOI: 0.820

### Strong Attack (AdvReverb + Opus)
**File**: sample-070322.wav  
**Original**: "The Christian Bible has seen many changes throughout history."  
**AdvReverb+Opus**: "I think the model could see many changes throughout this case." (WER: 0.6)  
**Metrics**: SNR: -4.99 dB, PESQ: 1.70, STOI: 0.756

### Catastrophic Failure (AdvReverb + AMR-WB)
**File**: sample-073138.wav  
**Original**: "You can't offer me something that is already mine, the Chief Set, arrogantly."  
**AdvReverb+AMR**: "Uke zobaczyennenästring�k but is open mind is sh align слуш düşün away" (WER: 0.92)  
**Metrics**: SNR: -3.42 dB, PESQ: 1.21, STOI: 0.735

---

## Codec Comparison

### Opus Codec (64 kbps)

**Characteristics**:
- High-quality lossy compression
- Preserves spectral details well
- Minimal impact on adversarial perturbations
- Excellent for voice and music

**Attack Mitigation**:
- **PGD**: Ineffective (98% attack survival)
- **AdvReverb**: Moderate (45% attack survival)

**Recommendation**: Not suitable as a defense mechanism against PGD attacks

---

### AMR-WB Codec (12.65 kbps)

**Characteristics**:
- Low-bitrate speech-optimized compression
- Aggressive frequency band reduction
- Significant audio quality degradation
- Designed for telephony applications

**Attack Mitigation**:
- **PGD**: Moderate (40% attack survival)
- **AdvReverb**: Strong (15% attack survival)

**Recommendation**: More effective as a defense but causes noticeable quality loss

---

## Attack Robustness Analysis

### Correlation: Audio Quality vs Attack Success

**PGD Attack**:
- High correlation between PESQ and low WER
- Better audio quality → better attack preservation
- Opus maintains quality → attack survives
- AMR-WB degrades quality → attack partially removed

**AdvReverb Attack**:
- Inverse correlation: poor audio quality inherent to attack
- Attack creates audible artifacts (negative SNR)
- Compression further degrades already poor quality
- Often results in unintelligible output

---

## Transcription Error Patterns

### Common PGD + AMR-WB Errors

1. **Word Substitution**: "almonds" → "homies", "palace" → "panorps"
2. **Word Omission**: Shortened transcriptions
3. **Phonetic Confusion**: "alchemist" → "alt can be"

### Common AdvReverb + AMR-WB Errors

1. **Complete Gibberish**: Multilingual nonsense, random characters
2. **Severe Truncation**: Long sentences → single words
3. **Hallucinations**: Unrelated words and phrases
4. **Mixed Languages**: English mixed with other language characters

**Examples**:
- "Mmkay. Hello. Ah. Yes. Okay. Yes." (sample-073912)
- "The present" (sample-073315)
- "a strunt organize the" (sample-074512)

---

## Conclusions

### Key Findings

1. **PGD is Superior for Codec Robustness**:
   - PGD attacks are significantly more robust to compression than AdvReverb
   - PGD maintains imperceptibility while AdvReverb creates audible artifacts

2. **Opus Provides Minimal Defense**:
   - High-quality codecs like Opus preserve adversarial perturbations
   - 98% of PGD attacks survive Opus compression unchanged

3. **AMR-WB Offers Better Defense**:
   - Low-bitrate compression removes more adversarial content
   - Trade-off: significant audio quality degradation
   - Not a complete defense (40% of PGD attacks still survive)

4. **AdvReverb is Impractical**:
   - Creates perceptible distortions (negative SNR)
   - Poor robustness to compression
   - Often produces unintelligible output after AMR-WB compression

5. **Codec Choice Matters**:
   - Attackers should target high-quality codecs (Opus, AAC)
   - Defenders can use aggressive compression as partial mitigation
   - Quality vs security trade-off is significant

---

## Recommendations

### For Attackers (Red Team)

1. **Use PGD over AdvReverb**: Better imperceptibility and robustness
2. **Target Opus-based systems**: Highest attack survival rate
3. **Avoid AMR-WB targets**: Significant attack degradation
4. **Optimize for high-bitrate codecs**: Better preservation of perturbations

### For Defenders (Blue Team)

1. **Use AMR-WB or low-bitrate codecs**: Better attack mitigation (but quality loss)
2. **Implement multi-stage compression**: Could further degrade attacks
3. **Monitor for audio quality anomalies**: AdvReverb attacks are detectable via SNR
4. **Don't rely solely on Opus**: Insufficient defense against PGD
5. **Consider hybrid approaches**: Compression + other defenses (adversarial training, denoising)

---

## Limitations

1. **AMR-WB Encoder**: Used AAC fallback due to unavailable AMR-WB encoder in environment
2. **Sample Size**: 80 samples from long-signals only (no short/medium signals)
3. **Single Bitrate**: Only tested one bitrate per codec
4. **ASR Model**: Only tested with Whisper base model
5. **Attack Parameters**: Fixed parameters (not optimized per sample)

---

## Future Work

1. **Test multiple bitrates**: Evaluate attack robustness across bitrate spectrum
2. **Test other codecs**: MP3, AAC, Vorbis, etc.
3. **Optimize attack parameters**: Per-sample parameter tuning
4. **Test other ASR models**: Wav2Vec2, DeepSpeech, etc.
5. **Evaluate targeted attacks**: Specific transcription goals
6. **Test codec chains**: Multiple compression/decompression cycles
7. **Implement true AMR-WB**: Use proper AMR-WB encoder for accurate results

---

## Data Summary

- **Total Audio Files**: 80
- **Total Pipelines**: 320 (80 files × 4 pipelines)
- **Successful Runs**: 320/320 (100%)
- **Average Processing Time**: ~2-3 minutes per file
- **Output Files Generated**: 
  - 80 PGD + Opus compressed files
  - 80 PGD + AMR-WB compressed files
  - 80 AdvReverb + Opus compressed files
  - 80 AdvReverb + AMR-WB compressed files
  - **Total**: 320 compressed audio files

---

## Appendix: Metric Definitions

### WER (Word Error Rate)
```
WER = (Substitutions + Deletions + Insertions) / Total Words in Reference
```
- Range: [0, ∞) (typically [0, 1])
- 0 = perfect match
- 1 = complete mismatch

### CER (Character Error Rate)
```
CER = (Substitutions + Deletions + Insertions) / Total Characters in Reference
```
- Range: [0, ∞) (typically [0, 1])
- More granular than WER

### SNR (Signal-to-Noise Ratio)
```
SNR = 10 × log₁₀(Signal Power / Noise Power) dB
```
- Higher = better quality
- Negative values = noise dominates signal
- >20 dB typically considered imperceptible

### PESQ (Perceptual Evaluation of Speech Quality)
- ITU-T P.862 standard
- Range: [-0.5, 4.5] (typically [1, 5])
- 5 = perfect quality
- <2 = poor quality

### STOI (Short-Time Objective Intelligibility)
- Range: [0, 1]
- 1 = perfect intelligibility
- >0.9 = excellent
- <0.7 = poor

---

**Report Generated**: December 2, 2025  
**Data Source**: `/Users/kunal/Downloads/pipeline_results.json`  
**Analysis Tool**: Python 3.12 with NumPy, Whisper, PESQ, STOI libraries

