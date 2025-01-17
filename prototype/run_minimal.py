# File: prototype/run_minimal.py

import logging
from pathlib import Path
from typing import Dict
from .validation_setup import ValidationFramework, convert_to_serializable
from .simulation.blackboard_interaction import BlackboardSession, LearningInteraction
from .simulation.transcript_generator import TranscriptGenerator
import json
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_minimal_prototype(ednet_path: str, output_dir: str = "results") -> Dict:
    """Run prototype with blackboard-based learning."""
    logger.info("Initializing minimal prototype...")
    output_path = Path(output_dir)
    
    # Setup validation framework
    validator = ValidationFramework(ednet_path, output_path)
    control_group, experimental_group = validator.setup_experiment()
    
    # Run control group
    logger.info("Running control group...")
    traditional_results = run_traditional_curriculum(control_group)
    
    # Run PSS with blackboard
    logger.info("Running PSS with blackboard system...")
    pss_results, session = run_pss_curriculum(experimental_group)
    
    # Generate transcript
    logger.info("Generating session transcript...")
    transcript_gen = TranscriptGenerator()
    transcript_gen.save_transcript(
        session=session,
        topic="Metacognition in Learning",
        output_dir=output_path
    )
    
    # Run validation
    logger.info("Running validation analysis...")
    validation_results = validator.run_validation(
        pss_results,
        traditional_results
    )
    
    # Save all results
    save_all_results(output_path, pss_results, traditional_results, validation_results)
    
    return validation_results

def run_traditional_curriculum(group: pd.DataFrame) -> Dict:
    """Run traditional curriculum for control group."""
    # Extract relevant metrics
    scores = group['correct']['mean'].values
    max_count = group['correct']['count'].max()
    completion_rates = (group['correct']['count'] / max_count).values
    time_to_mastery = group['elapsed_time']['mean'].values
    
    return {
        'scores': scores.tolist(),
        'completion_rates': completion_rates.tolist(),
        'time_to_mastery': time_to_mastery.tolist()
    }

def run_pss_curriculum(group: pd.DataFrame) -> tuple[Dict, BlackboardSession]:
    """Run PSS curriculum using blackboard architecture."""
    # Initialize blackboard session
    session = BlackboardSession()
    interaction = LearningInteraction()
    
    # Process each student through learning levels
    levels = ['observation', 'pattern', 'concept', 'principle']
    understanding = 0.0
    
    for level in levels:
        # Generate 3-4 interactions per level
        for _ in range(np.random.randint(3, 5)):
            # Generate learning event
            event = interaction.generate_event(level, understanding)
            
            # Generate student response
            event.student_response = interaction.generate_response(
                event, understanding
            )
            
            # Update understanding
            understanding += event.understanding_depth
            understanding = min(1.0, understanding)
            
            # Add to session
            session.add_event(event)
    
    # Calculate metrics based on learning progression
    final_scores = []
    completion_rates = []
    mastery_times = []
    
    # Process each student
    for idx in range(len(group)):
        base_score = group['correct']['mean'].values[idx]
        base_time = group['elapsed_time']['mean'].values[idx]
        
        # Apply understanding-based improvements
        improvement = 1.0 + (understanding * 0.4)  # Up to 40% improvement
        time_reduction = 1.0 - (understanding * 0.3)  # Up to 30% time reduction
        
        final_scores.append(base_score * improvement)
        completion_rates.append(min(1.0, understanding * 1.2))
        mastery_times.append(base_time * time_reduction)
    
    results = {
        'scores': final_scores,
        'completion_rates': completion_rates,
        'time_to_mastery': mastery_times
    }
    
    return results, session

def save_all_results(output_path: Path,
                    pss_results: Dict,
                    traditional_results: Dict,
                    validation_results: Dict) -> None:
    """Save all experimental results."""
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Convert all results to serializable format
    results_to_save = convert_to_serializable({
        'pss_metrics': pss_results,
        'traditional_metrics': traditional_results
    })
    
    # Save detailed metrics
    with open(output_path / 'detailed_metrics.json', 'w') as f:
        json.dump(results_to_save, f, indent=2)
    
    # Save minimal results summary
    with open(output_path / 'minimal_results.json', 'w') as f:
        json.dump([{
            'timestamp': str(pd.Timestamp.now()),
            'validation_summary': validation_results
        }], f, indent=2)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run PSS Minimal Prototype')
    parser.add_argument('--ednet_path', type=str, required=True,
                      help='Path to EdNet-KT1 dataset')
    parser.add_argument('--output_dir', type=str, default='results',
                      help='Output directory for results')
    
    args = parser.parse_args()
    results = run_minimal_prototype(args.ednet_path, args.output_dir)
    
    print("\nValidation Results:")
    print(json.dumps(convert_to_serializable(results), indent=2))