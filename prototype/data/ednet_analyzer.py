# File: prototype/data/ednet_analyzer.py

import pandas as pd
import numpy as np
from pathlib import Path
import json
from typing import Dict, Set, List
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class EdNetAnalyzer:
    """Analyzes EdNet-KT1 dataset to extract knowledge structure."""
    
    def __init__(self, ednet_path: str):
        self.ednet_path = ednet_path
        self.data = None
        self.knowledge_tags = set()
        self.concept_relationships = defaultdict(lambda: defaultdict(float))
        self.success_rates = {}
        self.prerequisite_strengths = defaultdict(lambda: defaultdict(float))
        
    def analyze_structure(self) -> Dict:
        """Extract knowledge structure from EdNet data."""
        logger.info("Loading EdNet data...")
        self.data = pd.read_csv(self.ednet_path)
        
        # Extract unique knowledge tags
        self.knowledge_tags = set(self.data['knowledge_tag'].unique())
        
        # Calculate success rates
        self._calculate_success_rates()
        
        # Analyze concept relationships
        self._analyze_concept_relationships()
        
        # Analyze prerequisites
        self._analyze_prerequisites()
        
        # Generate topic structure
        structure = self._generate_topic_structure()
        
        return structure
    
    def _calculate_success_rates(self) -> None:
        """Calculate success rates for each concept."""
        for tag in self.knowledge_tags:
            tag_data = self.data[self.data['knowledge_tag'] == tag]
            self.success_rates[tag] = {
                'correct_rate': tag_data['correct'].mean(),
                'attempts': len(tag_data),
                'avg_time': tag_data['elapsed_time'].mean()
            }
    
    def _analyze_concept_relationships(self) -> None:
        """Analyze relationships between concepts based on transitions."""
        total_transitions = 0
        
        # Analyze transitions between concepts
        for _, user_data in self.data.groupby('user_id'):
            user_data = user_data.sort_values('elapsed_time')
            prev_tag = None
            
            for tag in user_data['knowledge_tag']:
                if prev_tag is not None and prev_tag != tag:
                    self.concept_relationships[prev_tag][tag] += 1
                    total_transitions += 1
                prev_tag = tag
        
        # Normalize relationship strengths
        if total_transitions > 0:
            for tag1 in self.concept_relationships:
                for tag2 in self.concept_relationships[tag1]:
                    self.concept_relationships[tag1][tag2] /= total_transitions
    
    def _analyze_prerequisites(self) -> None:
        """Analyze prerequisite relationships through performance patterns."""
        for tag in self.knowledge_tags:
            tag_users = set(self.data[self.data['knowledge_tag'] == tag]['user_id'])
            
            for potential_prereq in self.knowledge_tags:
                if potential_prereq != tag:
                    prereq_success = []
                    tag_success = []
                    
                    for user_id in tag_users:
                        user_data = self.data[self.data['user_id'] == user_id]
                        
                        # Get success rates before attempting the target concept
                        prereq_attempts = user_data[
                            user_data['knowledge_tag'] == potential_prereq
                        ]['correct'].tolist()
                        
                        tag_attempts = user_data[
                            user_data['knowledge_tag'] == tag
                        ]['correct'].tolist()
                        
                        if prereq_attempts and tag_attempts:
                            prereq_success.append(np.mean(prereq_attempts))
                            tag_success.append(np.mean(tag_attempts))
                    
                    if prereq_success and tag_success:
                        # Calculate correlation between prerequisite success and concept success
                        correlation = np.corrcoef(prereq_success, tag_success)[0,1]
                        self.prerequisite_strengths[tag][potential_prereq] = max(0, correlation)
    
    def _generate_topic_structure(self) -> Dict:
        """Generate topic structure based on analysis."""
        structure = {"concepts": {}, "relationships": {}}
        
        # Generate concept information
        for tag in self.knowledge_tags:
            # Calculate difficulty from success rate
            difficulty = 1 - self.success_rates[tag]['correct_rate']
            
            # Find prerequisites (strongest prerequisite relationships)
            prerequisites = [
                prev_tag for prev_tag, strength in 
                sorted(self.prerequisite_strengths[tag].items(),
                      key=lambda x: x[1], reverse=True)
                if strength > 0.1  # Minimum correlation threshold
            ]
            
            structure["concepts"][tag] = {
                "difficulty": float(difficulty),
                "prerequisites": prerequisites,
                "avg_time": float(self.success_rates[tag]['avg_time']),
                "total_attempts": int(self.success_rates[tag]['attempts'])
            }
        
        # Generate relationship information
        for tag1 in self.knowledge_tags:
            for tag2 in self.knowledge_tags:
                if tag1 != tag2:
                    # Combine transition probability with prerequisite strength
                    strength = (
                        self.concept_relationships[tag1][tag2] +
                        self.prerequisite_strengths[tag2][tag1]
                    ) / 2
                    
                    if strength > 0.01:  # Minimum relationship strength
                        structure["relationships"][f"{tag1}_to_{tag2}"] = {
                            "connects": [tag1, tag2],
                            "strength": float(strength),
                            "bidirectional": bool(
                                self.concept_relationships[tag2][tag1] > 0.01 and
                                self.prerequisite_strengths[tag1][tag2] > 0.1
                            )
                        }
        
        return structure
    
    def save_structure(self, output_path: Path) -> None:
        """Save extracted knowledge structure."""
        structure = self._generate_topic_structure()
        
        # Calculate summary statistics
        summary = {
            "total_concepts": len(structure["concepts"]),
            "total_relationships": len(structure["relationships"]),
            "average_difficulty": float(np.mean([
                c["difficulty"] for c in structure["concepts"].values()
            ])),
            "average_relationship_strength": float(np.mean([
                r["strength"] for r in structure["relationships"].values()
            ]))
        }
        
        # Save main structure
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(structure, f, indent=2)
        
        # Save summary
        with open(output_path.parent / 'analysis_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
            
        logger.info(f"Saved knowledge structure to {output_path}")