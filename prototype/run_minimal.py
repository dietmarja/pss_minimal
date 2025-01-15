# File: prototype/run_minimal.py

def save_all_results(output_dir: Path, session, evaluation_results, adapter_results):
    """Save all results files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save basic metrics
    metrics_file = output_dir / "minimal_results.json"
    with metrics_file.open('w') as f:
        json.dump([{
            'timestamp': str(datetime.now()),
            'metrics': evaluation_results,
            'num_interactions': len(session),
            'ednet_sample_size': len(adapter_results)
        }], f, indent=2)
    
    # Save transcript
    transcript_file = output_dir / "session_transcript.txt"
    with transcript_file.open('w') as f:
        f.write(f"Session Transcript\nGenerated: {datetime.now()}\n\n")
        for interaction in session:
            f.write(f"[{interaction.timestamp}] Pattern Quality: {interaction.response_quality:.2f}\n")
            f.write(f"Pattern Type: {interaction.interaction_type}\n")
            f.write("-" * 40 + "\n")
    
    # Save curriculum design
    curriculum_file = output_dir / "curriculum_design.json"
    with curriculum_file.open('w') as f:
        json.dump({
            'pattern_evolution': [t.tolist() for t in session.state_trace],
            'quality_progression': [i.response_quality for i in session],
            'temporal_structure': [str(i.timestamp) for i in session]
        }, f, indent=2)
    
    # Save detailed metrics
    metrics_file = output_dir / "detailed_metrics.json"
    with metrics_file.open('w') as f:
        json.dump({
            'pattern_metrics': {
                'evolution_rate': evaluation_results['learning_effectiveness'],
                'coherence': evaluation_results['pattern_similarity'],
                'temporal_stability': evaluation_results['temporal_alignment']
            },
            'interaction_metrics': {
                'density': evaluation_results['engagement_score'],
                'pattern_count': len(session),
                'average_quality': np.mean([i.response_quality for i in session])
            }
        }, f, indent=2)