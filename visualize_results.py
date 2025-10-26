#!/usr/bin/env python3
"""
Visualization script for audio quality analysis results.
Creates plots for SNR, PESQ, and STOI metrics.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def load_results(json_file='audio_analysis_results.json'):
    """Load the analysis results from JSON file."""
    with open(json_file, 'r') as f:
        return json.load(f)

def plot_metrics_by_target(results):
    """Plot metrics grouped by target type."""
    # Filter valid results
    valid_results = [r for r in results if r['error'] is None]
    
    if not valid_results:
        print("No valid results to plot!")
        return
    
    # Group by target type
    targets = {}
    for result in valid_results:
        signal_type = result['signal_type']
        # Extract target (e.g., "short2medium" -> "medium")
        target = signal_type.split('2')[-1]
        
        if target not in targets:
            targets[target] = {'snr': [], 'pesq': [], 'stoi': []}
        
        # Filter out infinite SNR values
        if result['snr'] != float('inf') and not np.isnan(result['snr']):
            targets[target]['snr'].append(result['snr'])
        if not np.isnan(result['pesq']):
            targets[target]['pesq'].append(result['pesq'])
        if not np.isnan(result['stoi']):
            targets[target]['stoi'].append(result['stoi'])
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Audio Quality Metrics by Target Type', fontsize=16, fontweight='bold')
    
    target_names = sorted(targets.keys())
    x_pos = np.arange(len(target_names))
    
    # SNR plot
    ax1 = axes[0]
    snr_means = [np.mean(targets[t]['snr']) if targets[t]['snr'] else 0 for t in target_names]
    snr_stds = [np.std(targets[t]['snr']) if targets[t]['snr'] else 0 for t in target_names]
    
    bars1 = ax1.bar(x_pos, snr_means, yerr=snr_stds, capsize=5, alpha=0.7, 
                    color=['#FF6B6B', '#4ECDC4', '#95E1D3'])
    ax1.set_xlabel('Target Signal Type', fontsize=12, fontweight='bold')
    ax1.set_ylabel('SNR (dB)', fontsize=12, fontweight='bold')
    ax1.set_title('Signal-to-Noise Ratio', fontsize=13, fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([t.title() for t in target_names])
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars1, snr_means)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # PESQ plot
    ax2 = axes[1]
    pesq_means = [np.mean(targets[t]['pesq']) if targets[t]['pesq'] else 0 for t in target_names]
    pesq_stds = [np.std(targets[t]['pesq']) if targets[t]['pesq'] else 0 for t in target_names]
    
    bars2 = ax2.bar(x_pos, pesq_means, yerr=pesq_stds, capsize=5, alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4', '#95E1D3'])
    ax2.set_xlabel('Target Signal Type', fontsize=12, fontweight='bold')
    ax2.set_ylabel('PESQ Score', fontsize=12, fontweight='bold')
    ax2.set_title('Perceptual Evaluation of Speech Quality', fontsize=13, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([t.title() for t in target_names])
    ax2.set_ylim([0, 5.5])
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars2, pesq_means)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # STOI plot
    ax3 = axes[2]
    stoi_means = [np.mean(targets[t]['stoi']) if targets[t]['stoi'] else 0 for t in target_names]
    stoi_stds = [np.std(targets[t]['stoi']) if targets[t]['stoi'] else 0 for t in target_names]
    
    bars3 = ax3.bar(x_pos, stoi_means, yerr=stoi_stds, capsize=5, alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4', '#95E1D3'])
    ax3.set_xlabel('Target Signal Type', fontsize=12, fontweight='bold')
    ax3.set_ylabel('STOI Score', fontsize=12, fontweight='bold')
    ax3.set_title('Short-Time Objective Intelligibility', fontsize=13, fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([t.title() for t in target_names])
    ax3.set_ylim([0, 1.1])
    ax3.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars3, stoi_means)):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('metrics_by_target.png', dpi=300, bbox_inches='tight')
    print("Saved: metrics_by_target.png")
    
    return fig

def plot_metrics_by_original_type(results):
    """Plot metrics grouped by original signal type."""
    valid_results = [r for r in results if r['error'] is None]
    
    if not valid_results:
        return None
    
    # Group by original signal type
    signal_types = {}
    for result in valid_results:
        signal_type = result['signal_type']
        # Extract original (e.g., "short2medium" -> "short")
        original = signal_type.split('2')[0]
        
        if original not in signal_types:
            signal_types[original] = {'snr': [], 'pesq': [], 'stoi': []}
        
        if result['snr'] != float('inf') and not np.isnan(result['snr']):
            signal_types[original]['snr'].append(result['snr'])
        if not np.isnan(result['pesq']):
            signal_types[original]['pesq'].append(result['pesq'])
        if not np.isnan(result['stoi']):
            signal_types[original]['stoi'].append(result['stoi'])
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Audio Quality Metrics by Original Signal Type', fontsize=16, fontweight='bold')
    
    type_names = sorted(signal_types.keys())
    x_pos = np.arange(len(type_names))
    
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']
    
    # SNR plot
    ax1 = axes[0]
    snr_means = [np.mean(signal_types[t]['snr']) if signal_types[t]['snr'] else 0 for t in type_names]
    snr_stds = [np.std(signal_types[t]['snr']) if signal_types[t]['snr'] else 0 for t in type_names]
    bars1 = ax1.bar(x_pos, snr_means, yerr=snr_stds, capsize=5, alpha=0.7, color=colors[:len(type_names)])
    ax1.set_xlabel('Original Signal Type', fontsize=12, fontweight='bold')
    ax1.set_ylabel('SNR (dB)', fontsize=12, fontweight='bold')
    ax1.set_title('Signal-to-Noise Ratio', fontsize=13, fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([t.title() for t in type_names])
    ax1.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars1, snr_means):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height, f'{val:.1f}', 
                ha='center', va='bottom', fontweight='bold')
    
    # PESQ plot
    ax2 = axes[1]
    pesq_means = [np.mean(signal_types[t]['pesq']) if signal_types[t]['pesq'] else 0 for t in type_names]
    pesq_stds = [np.std(signal_types[t]['pesq']) if signal_types[t]['pesq'] else 0 for t in type_names]
    bars2 = ax2.bar(x_pos, pesq_means, yerr=pesq_stds, capsize=5, alpha=0.7, color=colors[:len(type_names)])
    ax2.set_xlabel('Original Signal Type', fontsize=12, fontweight='bold')
    ax2.set_ylabel('PESQ Score', fontsize=12, fontweight='bold')
    ax2.set_title('Perceptual Evaluation of Speech Quality', fontsize=13, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([t.title() for t in type_names])
    ax2.set_ylim([0, 5.5])
    ax2.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars2, pesq_means):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'{val:.2f}', 
                ha='center', va='bottom', fontweight='bold')
    
    # STOI plot
    ax3 = axes[2]
    stoi_means = [np.mean(signal_types[t]['stoi']) if signal_types[t]['stoi'] else 0 for t in type_names]
    stoi_stds = [np.std(signal_types[t]['stoi']) if signal_types[t]['stoi'] else 0 for t in type_names]
    bars3 = ax3.bar(x_pos, stoi_means, yerr=stoi_stds, capsize=5, alpha=0.7, color=colors[:len(type_names)])
    ax3.set_xlabel('Original Signal Type', fontsize=12, fontweight='bold')
    ax3.set_ylabel('STOI Score', fontsize=12, fontweight='bold')
    ax3.set_title('Short-Time Objective Intelligibility', fontsize=13, fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([t.title() for t in type_names])
    ax3.set_ylim([0, 1.1])
    ax3.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars3, stoi_means):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height, f'{val:.3f}', 
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('metrics_by_original_type.png', dpi=300, bbox_inches='tight')
    print("Saved: metrics_by_original_type.png")
    
    return fig

def create_summary_statistics(results):
    """Create a summary statistics visualization."""
    valid_results = [r for r in results if r['error'] is None]
    
    if not valid_results:
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    snr_vals = [r['snr'] for r in valid_results if r['snr'] != float('inf') and not np.isnan(r['snr'])]
    pesq_vals = [r['pesq'] for r in valid_results if not np.isnan(r['pesq'])]
    stoi_vals = [r['stoi'] for r in valid_results if not np.isnan(r['stoi'])]
    
    # Normalize values for comparison (0-1 scale)
    snr_norm = [(s - min(snr_vals)) / (max(snr_vals) - min(snr_vals)) if max(snr_vals) > min(snr_vals) else 0 for s in snr_vals]
    pesq_norm = [(p - 1) / 4 for p in pesq_vals]  # PESQ already 1-5
    stoi_norm = stoi_vals  # STOI already 0-1
    
    data_to_plot = [snr_norm, pesq_norm, stoi_norm]
    labels = ['SNR\n(normalized)', 'PESQ\n(normalized)', 'STOI']
    
    bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                    medianprops=dict(linewidth=2, color='black'),
                    boxprops=dict(alpha=0.7))
    
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    ax.set_ylabel('Normalized Score (0-1)', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Audio Quality Metrics', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('metrics_summary.png', dpi=300, bbox_inches='tight')
    print("Saved: metrics_summary.png")
    
    return fig

def main():
    print("Loading results...")
    results = load_results()
    
    print(f"Total results: {len(results)}")
    valid_results = [r for r in results if r['error'] is None]
    print(f"Valid results: {len(valid_results)}")
    
    print("\nGenerating visualizations...")
    
    # Create plots
    plot_metrics_by_target(results)
    plot_metrics_by_original_type(results)
    create_summary_statistics(results)
    
    print("\n" + "="*80)
    print("Visualization complete!")
    print("Generated files:")
    print("  - metrics_by_target.png")
    print("  - metrics_by_original_type.png")
    print("  - metrics_summary.png")
    print("="*80)

if __name__ == "__main__":
    main()
