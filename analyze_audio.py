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

def calculate_snr(original, noisy):
    """Calculate Signal-to-Noise Ratio (SNR) in dB."""
    # Calculate signal and noise power
    signal_power = np.mean(original ** 2)
    noise_power = np.mean((noisy - original) ** 2)
    
    if noise_power == 0:
        return float('inf')
    
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

def calculate_pesq_simple(original, processed, sr=16000):
    """
    Simplified PESQ-like metric calculation.
    PESQ (Perceptual Evaluation of Speech Quality) ranges from 1 (bad) to 5 (excellent).
    This is a simplified approximation since the actual PESQ requires the pypesq library.
    """
    # This is a placeholder - actual PESQ requires specialized library
    # For now, we'll use a correlation-based approximation
    if len(original) != len(processed):
        min_len = min(len(original), len(processed))
        original = original[:min_len]
        processed = processed[:min_len]
    
    # Correlation-based similarity
    correlation = np.corrcoef(original, processed)[0, 1]
    # Map correlation to 1-5 scale (PESQ range)
    pesq_approx = 1 + (correlation + 1) * 2  # Maps from [-1, 1] to [1, 5]
    
    return pesq_approx

def calculate_stoi(original, processed, sr=16000):
    """
    Simplified STOI-like metric calculation.
    STOI (Short-Time Objective Intelligibility) ranges from 0 to 1.
    This is a simplified approximation.
    """
    # Pad or trim to same length
    if len(original) != len(processed):
        min_len = min(len(original), len(processed))
        original = original[:min_len]
        processed = processed[:min_len]
    
    # Calculate spectral correlation
    # Get power spectral densities
    fft_orig = np.fft.rfft(original)
    fft_proc = np.fft.rfft(processed)
    
    # Calculate correlation between magnitude spectra
    mag_orig = np.abs(fft_orig)
    mag_proc = np.abs(fft_proc)
    
    # Normalize
    mag_orig_norm = mag_orig / (np.linalg.norm(mag_orig) + 1e-10)
    mag_proc_norm = mag_proc / (np.linalg.norm(mag_proc) + 1e-10)
    
    # Correlation
    stoi_score = np.dot(mag_orig_norm, mag_proc_norm)
    
    return max(0, min(1, stoi_score))

def load_audio_with_librosa(filepath):
    """Try to load audio using librosa, fallback to scipy if not available."""
    try:
        import librosa
        audio, sr = librosa.load(filepath, sr=16000)
        return audio, sr
    except ImportError:
        try:
            from scipy.io import wavfile
            sr, audio = wavfile.read(filepath)
            # Convert to mono if stereo
            if len(audio.shape) > 1:
                audio = np.mean(audio, axis=1)
            # Normalize to [-1, 1]
            audio = audio.astype(np.float32) / np.max(np.abs(audio))
            return audio, sr
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None, None

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
        # Load audio files
        orig_audio, sr_orig = load_audio_with_librosa(original_path)
        adv_audio, sr_adv = load_audio_with_librosa(adversarial_path)
        
        if orig_audio is None or adv_audio is None:
            results['error'] = "Failed to load audio files"
            return results
        
        # Ensure same sample rate
        if sr_orig != sr_adv:
            results['error'] = f"Sample rate mismatch: {sr_orig} vs {sr_adv}"
            return results
        
        # Ensure same length (pad or trim)
        min_len = min(len(orig_audio), len(adv_audio))
        orig_audio = orig_audio[:min_len]
        adv_audio = adv_audio[:min_len]
        
        # Calculate metrics
        snr = calculate_snr(orig_audio, adv_audio)
        pesq = calculate_pesq_simple(orig_audio, adv_audio, sr_orig)
        stoi = calculate_stoi(orig_audio, adv_audio, sr_orig)
        
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
