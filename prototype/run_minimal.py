# File: prototype/run_minimal.py

import torch
from transformers import AutoModel, AutoTokenizer
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prototype.simulation.emergent_simulation import EmergentSimulation
from prototype.evaluation.emergent_evaluation import EmergentEvaluator
from prototype.integration.ednet_adapter import EdNetAdapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    
    # Process first 100 interactions for quick testing
    sample_data = ednet_data.head(100)
    interactions = adapter.process_interactions(sample_data)
    
    # Run one simulation session
    logger.info("Running simulation session...")
    session = simulation.run_session()
    
    # Evaluate results
    logger.info("Evaluating results...")
    evaluation = evaluator.evaluate_pss_session(session)
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = {
        'timestamp': str(datetime.now()),
        'metrics': evaluation,
        'num_interactions': len(session),
        'ednet_sample_size': len(sample_data)
    }
    
    pd.DataFrame([results]).to_json(
        output_path / 'minimal_results.json',
        orient='records',
        indent=2
    )
    
    logger.info(f"Results saved to {output_path}")
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run minimal PSS prototype')
    parser.add_argument('--ednet_path', type=str, required=True,
                       help='Path to EdNet dataset')
    parser.add_argument('--output_dir', type=str, default='results',
                       help='Output directory for results')
    
    args = parser.parse_args()
    results = run_minimal_prototype(args.ednet_path, args.output_dir)
    print("\nEvaluation Results:")
    for metric, value in results['metrics'].items():
        print(f"{metric}: {value:.3f}")
