# File: prototype/data/run_analyzer.py

import logging
from pathlib import Path
import json
from prototype.data.ednet_analyzer import EdNetAnalyzer
from prototype.visualization.knowledge_visualizer import KnowledgeVisualizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_analysis(ednet_path: str, output_dir: str = "topics") -> None:
    """Run EdNet analysis and visualize results."""
    logger.info(f"Analyzing EdNet data from: {ednet_path}")
    
    # Run analysis
    output_path = Path(output_dir)
    analyzer = EdNetAnalyzer(ednet_path)
    structure = analyzer.analyze_structure()
    
    # Save structure
    analyzer.save_structure(output_path / "ednet_structure.json")
    
    # Create visualizations
    logger.info("Generating visualizations...")
    visualizer = KnowledgeVisualizer(output_path / "ednet_structure.json")
    visualizer.visualize_all(output_dir)
    
    # Print analysis summary
    print("\nEdNet Knowledge Structure Analysis")
    print("=" * 50)
    
    print("\nConcepts Found:", len(structure["concepts"]))
    print("-" * 30)
    
    # Sort concepts by difficulty
    concepts_by_difficulty = sorted(
        structure["concepts"].items(),
        key=lambda x: x[1]['difficulty']
    )
    
    for concept, data in concepts_by_difficulty:
        print(f"\nConcept: {concept}")
        print(f"Difficulty: {data['difficulty']:.2f}")
        print(f"Prerequisites: {', '.join(data['prerequisites'])}")
        print(f"Average Time: {data['avg_time']:.1f}s")
        print(f"Total Attempts: {data['total_attempts']}")
    
    print("\nStrong Relationships (strength > 0.2):")
    print("-" * 30)
    strong_relationships = [
        (name, data) for name, data in structure["relationships"].items()
        if data['strength'] > 0.2
    ]
    
    for name, data in sorted(strong_relationships, 
                           key=lambda x: x[1]['strength'],
                           reverse=True):
        print(f"\n{' -> '.join(data['connects'])}")
        print(f"Strength: {data['strength']:.2f}")
        print(f"Bidirectional: {data['bidirectional']}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze EdNet-KT1 dataset')
    parser.add_argument('ednet_path', type=str, help='Path to EdNet-KT1 dataset')
    parser.add_argument('--output_dir', type=str, default='topics',
                       help='Output directory for analysis files')
    
    args = parser.parse_args()
    run_analysis(args.ednet_path, args.output_dir)