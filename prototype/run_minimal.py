# File: prototype/run_minimal.py

import torch
from transformers import AutoModel, AutoTokenizer
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime
from typing import List, Dict, Optional
import json
import numpy as np
import os
import sys
import argparse  # Add this import


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from prototype.models.emergent_models import EmergentSession  # Add this import
from prototype.simulation.emergent_simulation import EmergentSimulation
from prototype.evaluation.emergent_evaluation import EmergentEvaluator
from prototype.integration.ednet_adapter import EdNetAdapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# File: prototype/run_minimal.py

def save_all_results(output_dir: Path, session: EmergentSession, 
                    evaluation_results: Dict, adapter_results: List) -> None:
    """Save all results files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save basic metrics
    metrics_file = output_dir / "minimal_results.json"
    with metrics_file.open('w') as f:
        json.dump([{
            'timestamp': str(datetime.now()),
            'metrics': evaluation_results,
            'num_interactions': len(session.interactions),  # Changed from len(session)
            'ednet_sample_size': len(adapter_results)
        }], f, indent=2)
    
    # Save transcript
    transcript_file = output_dir / "session_transcript.txt"
    with transcript_file.open('w') as f:
        f.write(f"Session Transcript\nGenerated: {datetime.now()}\n\n")
        for interaction in session.interactions:  # Using session.interactions
            f.write(f"[{interaction.timestamp}] Pattern Quality: {interaction.response_quality:.2f}\n")
            f.write(f"Pattern Type: {interaction.interaction_type}\n")
            f.write("-" * 40 + "\n")
    
    # Save curriculum design
    curriculum_file = output_dir / "curriculum_design.json"
    with curriculum_file.open('w') as f:
        json.dump({
            'pattern_evolution': [t.tolist() for t in session.state_trace],
            'quality_progression': [i.response_quality for i in session.interactions],
            'temporal_structure': [str(i.timestamp) for i in session.interactions]
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
                'pattern_count': len(session.interactions),
                'average_quality': np.mean([i.response_quality for i in session.interactions])
            }
        }, f, indent=2)


def run_minimal_prototype(ednet_path: str, output_dir: str):
    """Run minimal prototype with core functionality."""
    logger.info("Initializing minimal prototype...")
    
    # Initialize components
    simulation = EmergentSimulation()
    adapter = EdNetAdapter()
    evaluator = EmergentEvaluator()
    
    # Load sample EdNet data
    logger.info("Loading EdNet data...")
    ednet_data = adapter.load_ednet_data(ednet_path)
    sample_data = ednet_data.head(100)
    interactions = adapter.process_interactions(sample_data)
    
    # Run simulation session
    logger.info("Running simulation session...")
    session = simulation.run_session()
    
    # Evaluate results
    logger.info("Evaluating results...")
    evaluation = evaluator.evaluate_pss_session(session)
    
    # Save all results
    output_path = Path(output_dir)
    save_all_results(output_path, session, evaluation, interactions)
    
    logger.info(f"Results saved to {output_dir}")
    return evaluation

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run PSS minimal prototype')
    parser.add_argument('--ednet_path', type=str, required=True,
                       help='Path to EdNet dataset')
    parser.add_argument('--output_dir', type=str, default="results",
                       help='Output directory for results')
    
    args = parser.parse_args()
    results = run_minimal_prototype(args.ednet_path, args.output_dir)
    
    print("\nEvaluation Results:")
    for metric, value in results.items():
        print(f"{metric}: {value:.3f}")