# File: prototype/run_minimal.py

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from prototype.simulation.emergent_simulation import EmergentSimulation
from prototype.models.emergent_models import EmergentSession, DynamicInteraction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_results(output_path: Path, 
                session: EmergentSession,
                metrics: Dict) -> None:
    """Save session results."""
    results = {
        'timestamp': datetime.now().isoformat(),
        'session_id': session.id,
        'metrics': metrics,
        'state_evolution': [state.tolist() for state in session.state_trace],
        'interactions': [
            {
                'timestamp': i.timestamp.isoformat(),
                'speaker': i.speaker,
                'content': i.content,
                'topic': i.topic,
                'quality': i.response_quality
            }
            for i in session.interactions
        ]
    }
    
    # Save results
    output_path.mkdir(parents=True, exist_ok=True)
    with open(output_path / 'session_results.json', 'w') as f:
        json.dump(results, f, indent=2)

def run_minimal_prototype(output_dir: str = "results") -> Dict:
    """Run minimal prototype version."""
    logger.info("Initializing minimal prototype...")
    
    # Initialize components
    simulation = EmergentSimulation()
    output_path = Path(output_dir)
    
    # Run simulation
    logger.info("Running simulation session...")
    session = simulation.run_session()
    
    # Get metrics
    metrics = session.get_session_metrics()
    
    # Save results
    save_results(output_path, session, metrics)
    
    logger.info("Session completed. Results saved to %s", output_path)
    
    return metrics

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run PSS Minimal Prototype')
    parser.add_argument('--output_dir', type=str, default='results',
                       help='Output directory for results')
    
    args = parser.parse_args()
    results = run_minimal_prototype(args.output_dir)
    
    print("\nSession Metrics:")
    for metric, value in results.items():
        print(f"{metric}: {value}")