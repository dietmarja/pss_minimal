# File: run_system.py

import logging
from pathlib import Path
import torch
from datetime import datetime

# Import our components
from emergent_simulation import EmergentSimulation
from emergent_evaluation import EmergentEvaluator
from ednet_adapter import EdNetAdapter
from analysis_visualizer import AnalysisVisualizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pss_system(output_dir: str = "results"):
    """Run complete PSS system."""
    logger.info("Initializing PSS system...")
    
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize components
    simulation = EmergentSimulation()
    evaluator = EmergentEvaluator()
    adapter = EdNetAdapter()
    visualizer = AnalysisVisualizer(output_dir / "visualizations")
    
    # Step 1: Load and process mock data
    logger.info("Processing EdNet data...")
    mock_data = adapter.load_ednet_data("mock_ednet_kt1.csv")
    interactions = adapter.process_interactions(mock_data)
    
    # Step 2: Run simulation
    logger.info("Running simulation...")
    topics = ['algebra_basic', 'geometry_basic', 'arithmetic_basic']
    session_data = simulation.run_session(topics)
    
    # Step 3: Evaluate results
    logger.info("Evaluating results...")
    evaluation_results = evaluator.evaluate_pss_session(session_data)
    
    # Step 4: Generate visualizations
    logger.info("Generating visualizations...")
    visualizer.visualize_learning_patterns(
        [interaction.embedding for interaction in session_data],
        [interaction.embedding for interaction in interactions[:len(session_data)]]
    )
    
    # Step 5: Save results
    results = {
        'timestamp': str(datetime.now()),
        'evaluation_metrics': evaluation_results,
        'simulation_metrics': simulation.get_session_metrics(),
        'num_interactions': len(session_data)
    }
    
    # Print results
    print("\nEvaluation Results:")
    for metric, value in evaluation_results.items():
        print(f"{metric}: {value:.3f}")
    
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run PSS System')
    parser.add_argument('--output_dir', type=str, default='results',
                       help='Output directory for results')
    
    args = parser.parse_args()
    results = run_pss_system(args.output_dir)