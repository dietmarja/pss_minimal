# File: prototype/data/generate_mock_ednet.py

import pandas as pd
import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__)

# Define knowledge concepts and their prerequisites
KNOWLEDGE_STRUCTURE = {
    'algebra_basics': {
        'prerequisites': [],
        'difficulty': 0.3
    },
    'linear_equations': {
        'prerequisites': ['algebra_basics'],
        'difficulty': 0.5
    },
    'quadratic_equations': {
        'prerequisites': ['linear_equations'],
        'difficulty': 0.7
    },
    'function_analysis': {
        'prerequisites': ['quadratic_equations'],
        'difficulty': 0.8
    }
}

def generate_mock_ednet(n_students: int = 1000, 
                       n_questions_per_student: int = 50,
                       output_file: str = "mock_ednet_kt1.csv") -> None:
    """Generate mock EdNet-KT1 data."""
    
    logger.info(f"Generating mock data for {n_students} students")
    
    data = []
    knowledge_tags = list(KNOWLEDGE_STRUCTURE.keys())
    
    for user_id in range(n_students):
        # Track student's knowledge level for each concept
        knowledge_levels = {tag: 0.0 for tag in knowledge_tags}
        
        for q_idx in range(n_questions_per_student):
            # Select knowledge tag based on prerequisites
            available_tags = [
                tag for tag in knowledge_tags
                if all(knowledge_levels[prereq] > 0.5 
                      for prereq in KNOWLEDGE_STRUCTURE[tag]['prerequisites'])
            ]
            
            if not available_tags:
                available_tags = ['algebra_basics']
                
            tag = np.random.choice(available_tags)
            
            # Generate question attempt
            difficulty = KNOWLEDGE_STRUCTURE[tag]['difficulty']
            knowledge_level = knowledge_levels[tag]
            
            # Probability of correct answer based on knowledge and difficulty
            p_correct = (knowledge_level + 0.1) / (difficulty + 0.2)
            correct = np.random.random() < p_correct
            
            # Generate elapsed time (more time for difficult questions)
            base_time = 30 + (difficulty * 60)  # 30s to 90s base time
            elapsed_time = int(base_time * (1 + np.random.exponential(0.5)))
            
            # Record interaction
            data.append({
                'user_id': user_id,
                'question_id': len(data),  # unique question ID
                'correct': int(correct),
                'elapsed_time': elapsed_time,
                'knowledge_tag': tag
            })
            
            # Update knowledge level
            if correct:
                knowledge_levels[tag] = min(1.0, knowledge_levels[tag] + 0.1)
    
    # Convert to DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    
    logger.info(f"Generated {len(df)} interactions")
    logger.info(f"Saved to {output_file}")
    
    # Print summary statistics
    print("\nMock EdNet-KT1 Dataset Summary")
    print("=" * 40)
    print(f"Total Students: {n_students}")
    print(f"Total Interactions: {len(df)}")
    print(f"Knowledge Tags: {', '.join(knowledge_tags)}")
    print("\nCorrect Answer Rates by Concept:")
    for tag in knowledge_tags:
        tag_data = df[df['knowledge_tag'] == tag]
        print(f"{tag}: {tag_data['correct'].mean():.2f}")
    print("\nAverage Time by Concept (seconds):")
    for tag in knowledge_tags:
        tag_data = df[df['knowledge_tag'] == tag]
        print(f"{tag}: {tag_data['elapsed_time'].mean():.0f}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate_mock_ednet()