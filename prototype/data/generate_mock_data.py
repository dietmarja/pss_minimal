# File: prototype/data/generate_mock_data.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_mock_ednet_data(num_students: int = 100, 
                           interactions_per_student: int = 50) -> pd.DataFrame:
    """Generate mock EdNet-KT1 data for testing."""
    logger.info(f"Generating mock data for {num_students} students")
    
    data = []
    timestamp = datetime.now()
    
    for user_id in range(num_students):
        # Simulate learning progression
        base_knowledge = np.random.random()  # Initial knowledge level
        learning_rate = np.random.random() * 0.1  # Individual learning rate
        
        for i in range(interactions_per_student):
            # Knowledge increases with each interaction
            current_knowledge = min(1.0, base_knowledge + (i * learning_rate))
            
            # Generate interaction data
            interaction = {
                'user_id': user_id,
                'timestamp': timestamp + timedelta(minutes=i*5),
                'question_id': np.random.randint(1, 100),
                'correct': np.random.random() < current_knowledge,  # Probability based on knowledge
                'elapsed_time': np.random.randint(10, 300),  # 10-300 seconds
                'concept_id': np.random.randint(1, 10),
                'prior_questions': i,
                'avg_score': current_knowledge
            }
            data.append(interaction)
            
    df = pd.DataFrame(data)
    logger.info(f"Generated {len(df)} total interactions")
    
    return df

if __name__ == "__main__":
    # Generate mock data
    mock_data = generate_mock_ednet_data()
    
    # Save to CSV
    output_file = "mock_ednet_kt1.csv"
    mock_data.to_csv(output_file, index=False)
    logger.info(f"Saved mock data to {output_file}")

    # Display sample
    print("\nSample of generated data:")
    print(mock_data.head())
    print("\nData summary:")
    print(mock_data.describe())