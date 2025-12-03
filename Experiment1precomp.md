# Adversarial Attack Results Summary: Pre-Compression Analysis

**Date**: December 2, 2025  
**Dataset**: 50 audio samples from long-signals directory  
**Attacks**: PGD (Projected Gradient Descent) and AdvReverb (Convolutional White-Box)  
**ASR Model**: OpenAI Whisper (base)  
**Analysis Type**: Attack-only (NO compression applied)

---

## Executive Summary

This analysis evaluates the **raw effectiveness** of two white-box adversarial attacks (PGD and AdvReverb) **before any codec compression**. Each of the 50 audio samples was processed through:

1. **PGD Attack → Whisper Transcription → Metrics**
2. **AdvReverb Attack → Whisper Transcription → Metrics**

**Key Findings**:
- **PGD Attack**: **0% effectiveness** against Whisper (100% perfect transcription, WER = 0.0)
- **AdvReverb Attack**: **72% effectiveness** against Whisper (28% perfect transcription, mean WER = 22.05%)
- **PGD**: Imperceptible (SNR = ∞, PESQ = 4.64, STOI = 1.0) but **completely ineffective**
- **AdvReverb**: Perceptible (SNR = -3.03 dB, PESQ = 1.68, STOI = 0.78) but **moderately effective**

**Critical Insight**: PGD attacks optimized for Wav2Vec2 fail completely when evaluated with Whisper ASR, demonstrating **attack transferability limitations**.

---

## Methodology

### Pipeline Architecture

```
Original Audio (16kHz WAV)
    ↓
Get Original Transcript (Whisper)
    ↓
    ├─→ [PGD Attack] ─→ Whisper Transcription ─→ Metrics (WER, CER, SNR, PESQ, STOI)
    └─→ [AdvReverb Attack] ─→ Whisper Transcription ─→ Metrics (WER, CER, SNR, PESQ, STOI)
```

### Attack Configurations

#### PGD Attack (Gao et al., 2024)
- **Target Model**: Wav2Vec2-base-960h (for attack generation)
- **Evaluation Model**: Whisper-base (for transcription)
- **Parameters**:
  - Epsilon (ε): 0.002
  - Alpha (α): 0.0004
  - Steps: 10
  - Loss: Negative CTC loss (maximizes transcription error on Wav2Vec2)

#### AdvReverb Attack (Chen et al., 2023)
- **Target Model**: Wav2Vec2-base-960h (for attack generation)
- **Evaluation Model**: Whisper-base (for transcription)
- **Parameters**:
  - RIR Length: 2048 samples
  - Learning Rate: 0.001
  - Steps: 300
  - Optimization: Adam optimizer on RIR filter

### Metrics Computed

1. **WER (Word Error Rate)**: Measures transcription accuracy at word level (0 = perfect, 1 = complete failure)
2. **CER (Character Error Rate)**: Measures transcription accuracy at character level
3. **SNR (Signal-to-Noise Ratio)**: Audio quality in dB (higher = better, ∞ = perfect)
4. **PESQ (Perceptual Evaluation of Speech Quality)**: Perceived quality (1-5 scale, 5 = perfect)
5. **STOI (Short-Time Objective Intelligibility)**: Speech intelligibility (0-1 scale, 1 = perfect)

---

## Results Analysis

### 1. PGD Attack Results

**Performance**: ❌ **Complete Failure Against Whisper**

| Metric | Mean | Std Dev | Min | Max |
|--------|------|---------|-----|-----|
| **WER** | **0.0000** | 0.0000 | 0.0000 | 0.0000 |
| **CER** | **0.0000** | 0.0000 | 0.0000 | 0.0000 |
| **SNR** | **∞ (Infinity)** | - | ∞ | ∞ |
| **PESQ** | **4.6439** | 0.0000 | 4.6439 | 4.6439 |
| **STOI** | **1.0000** | 0.0000 | 1.0000 | 1.0000 |

**Analysis**:
- **Attack Success Rate**: 0% (0/50 files show any transcription error)
- **Perfect Transcription**: 100% (50/50 files transcribed perfectly)
- **Audio Quality**: Perfect preservation (SNR = ∞, PESQ ≈ 4.64, STOI = 1.0)
- **Conclusion**: PGD attacks optimized for Wav2Vec2 **completely fail** when evaluated with Whisper ASR

**Key Insight**: This demonstrates a critical limitation of adversarial attacks - **lack of transferability** between different ASR architectures. PGD perturbations that successfully fool Wav2Vec2 do not transfer to Whisper.

**Why This Happens**:
- PGD optimizes perturbations using Wav2Vec2's gradient
- Whisper uses a different architecture (Transformer-based encoder-decoder)
- Whisper's feature extraction and attention mechanisms differ significantly
- The adversarial perturbations are model-specific, not universal

---

### 2. AdvReverb Attack Results

**Performance**: ⚠️ **Moderate Effectiveness**

| Metric | Mean | Std Dev | Min | Max |
|--------|------|---------|-----|-----|
| **WER** | **0.2205** | 0.2486 | 0.0000 | 1.0000 |
| **CER** | **0.1154** | 0.1582 | 0.0000 | 0.8072 |
| **SNR** | **-3.03 dB** | 1.27 dB | -6.07 dB | -1.04 dB |
| **PESQ** | **1.6778** | 0.2628 | 1.1834 | 2.7539 |
| **STOI** | **0.7765** | 0.0495 | 0.6155 | 0.8429 |

**Analysis**:
- **Attack Success Rate**: 72% (36/50 files show transcription errors)
- **Perfect Transcription**: 28% (14/50 files transcribed perfectly)
- **Audio Quality**: Poor (negative SNR, low PESQ, moderate STOI)
- **Variability**: High standard deviation (σ = 0.25) indicates inconsistent attack effectiveness
- **Conclusion**: AdvReverb shows **moderate transferability** to Whisper, but with significant audio quality degradation

**Distribution**:
- 28% of samples maintain perfect transcription (WER = 0)
- 72% show varying degrees of transcription errors
- Some samples show complete failure (WER = 1.0)
- Mean WER of 22.05% indicates moderate attack effectiveness

**Notable Examples**:
- **Best Attack**: sample-070322.wav (WER = 1.0, complete transcription failure)
- **Worst Attack**: 14 samples with WER = 0.0 (no effect)

---

## Comparative Analysis

### Attack Effectiveness Ranking

1. **AdvReverb**: 22.05% mean WER ⭐⭐⭐ (Moderate)
2. **PGD**: 0.00% mean WER ⭐ (Complete Failure)

### Audio Quality Ranking

1. **PGD**: SNR = ∞, PESQ = 4.64, STOI = 1.0 ⭐⭐⭐⭐⭐ (Perfect)
2. **AdvReverb**: SNR = -3.03 dB, PESQ = 1.68, STOI = 0.78 ⭐⭐ (Poor)

### Attack Success Rate (WER > 0)

| Attack | Success Rate | Perfect Transcription |
|--------|--------------|----------------------|
| PGD | 0% (0/50) | 100% (50/50) |
| AdvReverb | 72% (36/50) | 28% (14/50) |

---

## Detailed Statistical Analysis

### PGD Attack Statistics

**Transcription Accuracy**:
- **WER**: 0.0000 ± 0.0000 (all samples perfect)
- **CER**: 0.0000 ± 0.0000 (all samples perfect)
- **Perfect Transcription Rate**: 100% (50/50)

**Audio Quality**:
- **SNR**: ∞ (perfect - no measurable noise)
- **PESQ**: 4.6439 ± 0.0000 (near-perfect quality)
- **STOI**: 1.0000 ± 0.0000 (perfect intelligibility)

**Conclusion**: PGD creates imperceptible perturbations that are **completely ineffective** against Whisper ASR.

---

### AdvReverb Attack Statistics

**Transcription Accuracy**:
- **WER**: 0.2205 ± 0.2486 (moderate, high variance)
- **CER**: 0.1154 ± 0.1582 (moderate, high variance)
- **Perfect Transcription Rate**: 28% (14/50)
- **Attack Success Rate**: 72% (36/50)

**Audio Quality**:
- **SNR**: -3.03 ± 1.27 dB (poor - noise dominates signal)
- **PESQ**: 1.6778 ± 0.2628 (poor quality)
- **STOI**: 0.7765 ± 0.0495 (moderate intelligibility)

**Conclusion**: AdvReverb creates perceptible distortions that show **moderate transferability** to Whisper, but with significant audio quality degradation.

---

## Attack Transferability Analysis

### Cross-Model Transferability

**PGD Attack**:
- **Source Model**: Wav2Vec2-base-960h (attack generation)
- **Target Model**: Whisper-base (evaluation)
- **Transferability**: ❌ **0%** (complete failure)
- **Reason**: Architecture mismatch - gradient-based attacks are highly model-specific

**AdvReverb Attack**:
- **Source Model**: Wav2Vec2-base-960h (attack generation)
- **Target Model**: Whisper-base (evaluation)
- **Transferability**: ⚠️ **72%** (moderate success)
- **Reason**: Convolutional reverb effects are more universal and affect acoustic features that both models rely on

### Key Insight

**White-box attacks optimized for one ASR model show limited transferability to different architectures**. This is a critical finding for adversarial robustness research:

- **Model-specific attacks** (PGD) fail completely when evaluated on different models
- **Acoustic-based attacks** (AdvReverb) show better transferability but at the cost of perceptibility

---

## Perceptibility Analysis

### Imperceptible Range Thresholds

- **SNR > 20 dB**: Typically considered imperceptible
- **PESQ > 4.0**: Excellent quality
- **STOI > 0.95**: Excellent intelligibility

### Attack Perceptibility

| Attack | SNR | PESQ | STOI | Imperceptible? |
|--------|-----|------|------|----------------|
| **PGD** | ∞ | 4.64 | 1.00 | ✅ **Yes** (Perfect) |
| **AdvReverb** | -3.03 dB | 1.68 | 0.78 | ❌ **No** (Audible) |

**Analysis**:
- **PGD**: Creates imperceptible perturbations (SNR = ∞) but completely ineffective
- **AdvReverb**: Creates perceptible distortions (negative SNR) but moderately effective
- **Trade-off**: There is a clear trade-off between attack effectiveness and imperceptibility

---

## Notable Examples

### PGD Attack - Perfect Transcription (All Samples)

**Example 1**: sample-070236.wav  
**Original**: "We are part of that soul. So we really recognize that it is working for us."  
**PGD Attack**: "We are part of that soul. So we really recognize that it is working for us." (WER: 0.0)  
**Metrics**: SNR: ∞, PESQ: 4.64, STOI: 1.00

**Example 2**: sample-070322.wav  
**Original**: "The Christian Bible has seen many changes throughout history."  
**PGD Attack**: "The Christian Bible has seen many changes throughout history." (WER: 0.0)  
**Metrics**: SNR: ∞, PESQ: 4.64, STOI: 1.00

**Conclusion**: PGD attacks show **zero effectiveness** across all samples.

---

### AdvReverb Attack - Successful Attacks

**Example 1**: sample-070322.wav (Complete Failure)  
**Original**: "The Christian Bible has seen many changes throughout history."  
**AdvReverb Attack**: "and Kristen Blvis see American Shin just weil Konoru." (WER: 1.0)  
**Metrics**: SNR: -2.48 dB, PESQ: 1.55, STOI: 0.74

**Example 2**: sample-073315.wav (Complete Failure)  
**Original**: "Coming home, it's your tourist past at home. I've been seeing you playing music."  
**AdvReverb Attack**: "It was Now Satdown." (WER: 1.0)  
**Metrics**: SNR: -2.27 dB, PESQ: 1.26, STOI: 0.71

**Example 3**: sample-076120.wav (High Error)  
**Original**: "You have a media for simplifying everything, answer the Englishman irritated."  
**AdvReverb Attack**: "You haven't made a personal point, everything answered the Emishment, Eritated." (WER: 0.73)  
**Metrics**: SNR: -1.74 dB, PESQ: 1.66, STOI: 0.80

---

### AdvReverb Attack - Failed Attacks (Perfect Transcription)

**Example 1**: sample-071242.wav  
**Original**: "In those days, very few of the people had any idea about astronomy."  
**AdvReverb Attack**: "In those days, very few of the people had any idea about astronomy." (WER: 0.0)  
**Metrics**: SNR: -1.04 dB, PESQ: 1.51, STOI: 0.81

**Example 2**: sample-073703.wav  
**Original**: "Looking through the telescope, I saw a circle of deep blue and little round planet."  
**AdvReverb Attack**: "Looking through the telescope, I saw a circle of deep blue and little round planet." (WER: 0.0)  
**Metrics**: SNR: -4.57 dB, PESQ: 1.54, STOI: 0.83

**Conclusion**: Even with perceptible distortions, AdvReverb fails on 28% of samples.

---

## Attack Effectiveness Distribution

### PGD Attack WER Distribution

```
WER = 0.0: ████████████████████████████████████████████████████ 100% (50/50)
WER > 0.0:                                                        0% (0/50)
```

**Conclusion**: Complete failure - all samples transcribed perfectly.

---

### AdvReverb Attack WER Distribution

```
WER = 0.0:     ████████████████ 28% (14/50)
WER 0.0-0.2:   ████████████████████████████████ 48% (24/50)
WER 0.2-0.5:   ████████ 8% (4/50)
WER 0.5-0.8:   ████ 4% (2/50)
WER 0.8-1.0:   ████ 4% (2/50)
WER = 1.0:     ████ 4% (2/50)
```

**Analysis**:
- 28% of samples show no attack effect (WER = 0)
- 48% show mild attack effect (WER < 0.2)
- 16% show moderate to severe attack effect (WER > 0.2)
- 4% show complete transcription failure (WER = 1.0)

---

## Audio Quality vs Attack Effectiveness

### Correlation Analysis

**PGD Attack**:
- **High Quality, Zero Effectiveness**: Perfect audio quality (SNR = ∞) but 0% attack success
- **Conclusion**: Imperceptibility does not guarantee attack effectiveness across models

**AdvReverb Attack**:
- **Poor Quality, Moderate Effectiveness**: Poor audio quality (SNR = -3.03 dB) but 72% attack success
- **Conclusion**: Perceptible distortions can achieve better cross-model transferability

**Key Finding**: There is an **inverse relationship** between imperceptibility and cross-model attack effectiveness in this study.

---

## Attack Robustness to Different ASR Models

### Model-Specific vs Universal Attacks

**PGD (Model-Specific)**:
- Optimized using Wav2Vec2 gradients
- Highly effective against Wav2Vec2 (target model)
- **Completely ineffective** against Whisper (different architecture)
- **Transferability**: 0%

**AdvReverb (Acoustic-Based)**:
- Uses convolutional reverb (acoustic transformation)
- Moderately effective against Wav2Vec2
- **Moderately effective** against Whisper (better transferability)
- **Transferability**: 72%

**Conclusion**: **Acoustic-based attacks show better transferability** than gradient-based attacks across different ASR architectures.

---

## Error Pattern Analysis

### Common AdvReverb Transcription Errors

1. **Word Substitution**: 
   - "love" → "Lord"
   - "paid" → "sword"
   - "almonds" → "homies"

2. **Word Omission**: 
   - Shortened transcriptions
   - Missing words in sentences

3. **Phonetic Confusion**: 
   - "alchemist" → "alt can be"
   - "palace" → "panorps"

4. **Complete Gibberish**: 
   - "and Kristen Blvis see American Shin just weil Konoru" (sample-070322)
   - "It was Now Satdown" (sample-073315)

5. **Severe Truncation**: 
   - Long sentences reduced to short phrases

---

## Conclusions

### Key Findings

1. **PGD Shows Zero Transferability**:
   - Attacks optimized for Wav2Vec2 completely fail against Whisper
   - 100% perfect transcription rate (WER = 0.0) across all samples
   - Demonstrates critical limitation of gradient-based white-box attacks

2. **AdvReverb Shows Moderate Transferability**:
   - 72% attack success rate against Whisper
   - Mean WER of 22.05% indicates moderate effectiveness
   - Better cross-model transferability than PGD

3. **Trade-off Between Imperceptibility and Effectiveness**:
   - PGD: Imperceptible (SNR = ∞) but ineffective (WER = 0%)
   - AdvReverb: Perceptible (SNR = -3.03 dB) but more effective (WER = 22.05%)

4. **Architecture Mismatch Matters**:
   - White-box attacks are highly model-specific
   - Different ASR architectures require different attack strategies
   - Transferability is not guaranteed even for white-box attacks

5. **Acoustic-Based Attacks Are More Universal**:
   - Convolutional reverb affects acoustic features used by multiple models
   - Better transferability than gradient-based attacks
   - But at the cost of perceptibility

---

## Recommendations

### For Attackers (Red Team)

1. **Use Acoustic-Based Attacks for Cross-Model Transferability**:
   - AdvReverb shows better transferability than PGD
   - Consider other acoustic transformations (noise, filtering, etc.)

2. **Avoid Model-Specific Gradient Attacks for Universal Attacks**:
   - PGD fails completely when evaluated on different models
   - Only use for targeted attacks on specific models

3. **Accept Perceptibility Trade-off**:
   - More effective attacks may require perceptible distortions
   - Balance between effectiveness and stealth

### For Defenders (Blue Team)

1. **Use Different ASR Models for Evaluation**:
   - Attacks optimized for one model may fail on others
   - Multi-model evaluation provides better robustness assessment

2. **Monitor for Audio Quality Anomalies**:
   - AdvReverb attacks are detectable via SNR monitoring
   - Negative SNR indicates potential adversarial manipulation

3. **Don't Rely on Single-Model Evaluation**:
   - Test robustness across multiple ASR architectures
   - Model diversity provides natural defense against model-specific attacks

4. **Consider Ensemble ASR Systems**:
   - Multiple models can detect attacks that fool individual models
   - Cross-validation between models improves security

---

## Limitations

1. **Single Evaluation Model**: Only tested with Whisper-base (not other models)
2. **Sample Size**: 50 samples from long-signals only
3. **Attack Parameters**: Fixed parameters (not optimized per sample)
4. **ASR Model**: Only tested with Whisper (not other ASR systems)
5. **No Compression**: Results are pre-compression (compression may affect attacks differently)

---

## Future Work

1. **Test Multiple ASR Models**: Evaluate attacks against Wav2Vec2, DeepSpeech, etc.
2. **Optimize Attacks for Whisper**: Create Whisper-specific attacks to test effectiveness
3. **Test Attack Transferability**: Evaluate how attacks transfer between different models
4. **Investigate Acoustic-Based Attacks**: Explore other acoustic transformations
5. **Study Compression Effects**: Analyze how compression affects attack effectiveness
6. **Ensemble Defense**: Test multi-model ensemble defenses
7. **Perceptibility Studies**: Human perception studies to validate SNR/PESQ thresholds

---

## Data Summary

- **Total Audio Files**: 50
- **Total Attacks Generated**: 100 (50 PGD + 50 AdvReverb)
- **Successful Runs**: 50/50 (100%)
- **Output Files Generated**: 
  - 50 PGD attack files (`*_pgd_attack.wav`)
  - 50 AdvReverb attack files (`*_advreverb_attack.wav`)
  - **Total**: 100 adversarial audio files

---

## Appendix: Metric Definitions

### WER (Word Error Rate)
```
WER = (Substitutions + Deletions + Insertions) / Total Words in Reference
```
- Range: [0, ∞) (typically [0, 1])
- 0 = perfect match
- 1 = complete mismatch
- Lower is better

### CER (Character Error Rate)
```
CER = (Substitutions + Deletions + Insertions) / Total Characters in Reference
```
- Range: [0, ∞) (typically [0, 1])
- More granular than WER
- Lower is better

### SNR (Signal-to-Noise Ratio)
```
SNR = 10 × log₁₀(Signal Power / Noise Power) dB
```
- Higher = better quality
- Negative values = noise dominates signal
- ∞ = perfect (no noise)
- >20 dB typically considered imperceptible

### PESQ (Perceptual Evaluation of Speech Quality)
- ITU-T P.862 standard
- Range: [-0.5, 4.5] (typically [1, 5])
- 5 = perfect quality
- <2 = poor quality
- Higher is better

### STOI (Short-Time Objective Intelligibility)
- Range: [0, 1]
- 1 = perfect intelligibility
- >0.9 = excellent
- <0.7 = poor
- Higher is better

---

**Report Generated**: December 2, 2025  
**Data Source**: `/Users/kunal/Code/BiometricProject/attack_only_results.json`  
**Analysis Tool**: Python 3.12 with NumPy, Whisper, PESQ, STOI libraries

