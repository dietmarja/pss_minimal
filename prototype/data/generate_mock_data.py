# File: prototype/data/generate_mock_data.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_mock_ednet_data(num_students=10, num_questions=20, output_path='mock_ednet_kt1.csv'):
    """Generate mock EdNet data for testing."""
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    # Questions represent different math concepts
    question_types = [
        'algebra_basic', 'algebra_advanced',
        'geometry_basic', 'geometry_advanced',
        'arithmetic_basic', 'arithmetic_advanced'
    ]
    
    for student_id in range(num_students):
        # Each student attempts multiple questions
        current_time = start_date + timedelta(days=student_id)
        student_skill = random.random()  # Random initial skill level
        
        for question_num in range(num_questions):
            # Simulate learning - skill improves over time
            student_skill = min(1.0, student_skill + random.random() * 0.1)
            
            # Generate question attempt
            question_type = random.choice(question_types)
            question_id = f"{question_type}_{random.randint(1, 5)}"
            
            # Calculate probability of correct answer
            correct_prob = student_skill * (0.5 + random.random() * 0.5)
            correct = random.random() < correct_prob
            
            # Response time between 10 and 300 seconds
            response_time = random.randint(10, 300)
            
            data.append({
                'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': f"student_{student_id}",
                'question_id': question_id,
                'correct': int(correct),
                'response_time': response_time,
                'topic': question_type
            })
            
            # Move time forward
            current_time += timedelta(minutes=random.randint(5, 30))
    
    # Create DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Generated mock data saved to {output_path}")
    print(f"Sample of generated data:")
    print(df.head())
    return df

if __name__ == "__main__":
    # Generate mock data
    generate_mock_ednet_data()