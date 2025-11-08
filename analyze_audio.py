#!/usr/bin/env python3
"""
Audio Quality Analysis Script
Analyzes SNR, PESQ, and STOI metrics for original vs adversarial audio samples.
"""

import os
import json
import numpy as np
from pathlib import Path
import random
from typing import Tuple

from scipy.signal import correlate
from pesq import pesq as pesq_metric
from pystoi.stoi import stoi as stoi_metric

# Configuration
TARGET_SR = 16000
NORMALIZE_PEAK = 0.99
MAX_ALIGNMENT_SHIFT_S = 0.5

def calculate_snr(original, noisy):
    """Calculate Signal-to-Noise Ratio (SNR) in dB."""
    # Calculate signal and noise power
    signal_power = np.mean(original ** 2)
    noise_power = np.mean((noisy - original) ** 2)
    
    if noise_power == 0:
        return float('inf')
    
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

def compute_pesq(reference: np.ndarray, degraded: np.ndarray, sr: int = TARGET_SR) -> float:
    """Compute PESQ (ITU-T P.862). Uses wideband mode for 16 kHz.
    Returns a float typically in [-0.5, 4.5].
    """
    # PESQ requires same length
    min_len = min(len(reference), len(degraded))
    reference = reference[:min_len]
    degraded = degraded[:min_len]
    return float(pesq_metric(sr, reference, degraded, 'wb'))

def compute_stoi(reference: np.ndarray, degraded: np.ndarray, sr: int = TARGET_SR) -> float:
    """Compute STOI (0..1)."""
    min_len = min(len(reference), len(degraded))
    reference = reference[:min_len]
    degraded = degraded[:min_len]
    return float(stoi_metric(reference, degraded, sr, extended=False))

def _peak_normalize(audio: np.ndarray, peak_target: float = NORMALIZE_PEAK) -> np.ndarray:
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio
    scale = peak_target / peak
    return (audio * scale).astype(np.float32)

def load_audio(filepath: str, target_sr: int = TARGET_SR) -> Tuple[np.ndarray, int]:
    """Load audio as mono at target_sr, float32, then peak-normalize."""
    import librosa
    audio, sr = librosa.load(filepath, sr=target_sr, mono=True)
    audio = _peak_normalize(audio, NORMALIZE_PEAK)
    return audio.astype(np.float32), sr

def align_signals(reference: np.ndarray, estimate: np.ndarray, sr: int = TARGET_SR,
                  max_shift_s: float = MAX_ALIGNMENT_SHIFT_S) -> Tuple[np.ndarray, np.ndarray]:
    """Align estimate to reference using cross-correlation within ±max_shift_s.
    Returns trimmed aligned copies of (reference, estimate).
    """
    max_shift = int(max_shift_s * sr)
    # limit to same length for correlation speed
    n = min(len(reference), len(estimate))
    ref = reference[:n]
    est = estimate[:n]
    # compute correlation around zero lag window
    corr_full = correlate(est, ref, mode='full')
    lags = np.arange(-len(ref) + 1, len(est))
    # restrict to lag window
    mask = (lags >= -max_shift) & (lags <= max_shift)
    corr = corr_full[mask]
    lag_window = lags[mask]
    best_lag = lag_window[np.argmax(corr)]

    if best_lag > 0:
        # est lags behind ref -> advance est
        est_aligned = est[best_lag:]
        ref_aligned = ref[:len(est_aligned)]
    elif best_lag < 0:
        # est ahead of ref -> delay est
        ref_aligned = ref[-best_lag:]
        est_aligned = est[:len(ref_aligned)]
    else:
        ref_aligned, est_aligned = ref, est

    m = min(len(ref_aligned), len(est_aligned))
    return ref_aligned[:m], est_aligned[:m]

def analyze_sample_pair(original_path, adversarial_path, original_signal_type, target_type):
    """Analyze a single original-adversarial pair."""
    results = {
        'original_file': os.path.basename(original_path),
        'adversarial_file': os.path.basename(adversarial_path),
        'signal_type': f"{original_signal_type}2{target_type}",
        'snr': None,
        'pesq': None,
        'stoi': None,
        'error': None
    }
    
    try:
        # Load audio files (mono, 16 kHz, normalized)
        orig_audio, sr_orig = load_audio(original_path)
        adv_audio, sr_adv = load_audio(adversarial_path)
        
        if orig_audio is None or adv_audio is None:
            results['error'] = "Failed to load audio files"
            return results
        
        # Ensure same sample rate
        if sr_orig != sr_adv:
            results['error'] = f"Sample rate mismatch: {sr_orig} vs {sr_adv}"
            return results
        
        # Align signals and trim
        orig_audio, adv_audio = align_signals(orig_audio, adv_audio, sr_orig, MAX_ALIGNMENT_SHIFT_S)
        
        # Calculate metrics
        snr = calculate_snr(orig_audio, adv_audio)
        pesq = compute_pesq(orig_audio, adv_audio, sr_orig)
        stoi = compute_stoi(orig_audio, adv_audio, sr_orig)
        
        results['snr'] = float(snr)
        results['pesq'] = float(pesq)
        results['stoi'] = float(stoi)
        
    except Exception as e:
        results['error'] = str(e)
    
    return results

def main():
    # Load the adversarial pairs JSON
    pairs_file = 'adversarial_pairs.json'
    if not os.path.exists(pairs_file):
        print(f"Error: {pairs_file} not found!")
        return
    
    with open(pairs_file, 'r') as f:
        data = json.load(f)
    
    # Base path for audio files
    base_path = Path("/Users/kunal/Downloads/adversarial_dataset-A/Adversarial-Examples")
    
    all_results = []
    
    print("Starting audio analysis...")
    print("="*80)
    
    # Process each signal type
    for signal_type, pairs in data.items():
        print(f"\nProcessing {signal_type}...")
        
        # Sample 10 files from each signal type (or all if less than 10)
        sample_size = min(10, len(pairs))
        sampled_pairs = random.sample(pairs, sample_size)
        
        print(f"  Analyzing {sample_size} samples from {len(pairs)} total...")
        
        for i, pair in enumerate(sampled_pairs, 1):
            original_file = pair['original']
            original_path = base_path / signal_type / "Original-examples" / original_file
            
            for adv_type, adv_file in pair['adversarial_samples'].items():
                # Determine target type from adversarial type
                if '2short' in adv_file:
                    target = 'short'
                elif '2medium' in adv_file:
                    target = 'medium'
                else:
                    target = 'long'
                
                adv_path = base_path / signal_type / adv_type / adv_file
                
                print(f"  [{i}/{sample_size}] {original_file} -> {target} target...", end=' ')
                
                # Analyze the pair
                result = analyze_sample_pair(
                    str(original_path),
                    str(adv_path),
                    signal_type.replace('-signals', ''),
                    target
                )
                
                if result['error']:
                    print(f"ERROR: {result['error']}")
                else:
                    print(f"SNR: {result['snr']:.2f} dB, PESQ: {result['pesq']:.2f}, STOI: {result['stoi']:.3f}")
                
                all_results.append(result)
    
    # Save results
    output_file = 'audio_analysis_results.json'
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "="*80)
    print(f"Analysis complete! Results saved to: {output_file}")
    print(f"Total pairs analyzed: {len(all_results)}")
    
    # Print summary statistics
    valid_results = [r for r in all_results if r['error'] is None]
    if valid_results:
        print("\nSummary Statistics:")
        print(f"  Valid results: {len(valid_results)}")
        snr_values = [r['snr'] for r in valid_results if r['snr'] != float('inf')]
        print(f"  Average SNR: {np.mean(snr_values):.2f} dB")
        print(f"  Average PESQ: {np.mean([r['pesq'] for r in valid_results]):.2f}")
        print(f"  Average STOI: {np.mean([r['stoi'] for r in valid_results]):.3f}")

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    main()
