# File: prototype/data/ednet_sampler.py

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict
import yaml
import logging

logger = logging.getLogger(__name__)

class EdNetSampler:
    """Handles systematic sampling from EdNet dataset."""
    
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.ednet_config = self.config['experiment']['ednet']
        
    def sample_groups(self, ednet_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Create matched experimental and control groups."""
        logger.info(f"Loading EdNet data from {ednet_path}")
        
        # Load data
        df = pd.read_csv(ednet_path)
        
        # Filter for minimum interactions per student
        interaction_counts = df.groupby('user_id').size()
        eligible_students = interaction_counts[
            interaction_counts >= self.ednet_config['min_interactions_per_student']
        ].index
        
        df_filtered = df[df['user_id'].isin(eligible_students)]
        
        # Calculate student proficiency metrics
        student_metrics = self._calculate_student_metrics(df_filtered)
        
        # Create matched groups
        control, experimental = self._create_matched_groups(student_metrics)
        
        logger.info(f"Created groups with {len(control)} students each")
        return self._get_student_data(df_filtered, control), self._get_student_data(df_filtered, experimental)
    
    def _calculate_student_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate comprehensive student metrics."""
        metrics = df.groupby('user_id').agg({
            'correct': ['mean', 'count'],
            'elapsed_time': ['mean', 'std'],
            'question_id': 'nunique'  # Topic coverage
        }).reset_index()
        
        # Add learning rate metric (improvement over time)
        learning_rates = []
        for student in metrics['user_id']:
            student_data = df[df['user_id'] == student]
            if len(student_data) >= 2:
                # Calculate rolling average of performance
                rolling_perf = student_data['correct'].rolling(5, min_periods=1).mean()
                learning_rates.append((rolling_perf.iloc[-1] - rolling_perf.iloc[0]))
            else:
                learning_rates.append(0)
        
        metrics['learning_rate'] = learning_rates
        return metrics
    
    def _create_matched_groups(self, metrics: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Create matched groups using stratified sampling."""
        group_size = self.ednet_config['control_group_size']
        
        # Create composite score for matching
        metrics['composite_score'] = (
            metrics['correct']['mean'] * 0.4 +
            metrics['learning_rate'] * 0.3 +
            (metrics['question_id'] / metrics['question_id'].max()) * 0.3
        )
        
        # Create stratification bins
        metrics['strata'] = pd.qcut(metrics['composite_score'], q=5, labels=False)
        
        # Sample from each stratum
        control_ids = []
        experimental_ids = []
        
        for stratum in range(5):
            stratum_students = metrics[metrics['strata'] == stratum]['user_id'].values
            if len(stratum_students) >= 2:  # Ensure we can split
                sampled = np.random.choice(
                    stratum_students,
                    size=min(group_size // 5, len(stratum_students) // 2),
                    replace=False
                )
                control_ids.extend(sampled)
                remaining = set(stratum_students) - set(sampled)
                experimental_ids.extend(
                    np.random.choice(list(remaining), size=len(sampled), replace=False)
                )
        
        return pd.DataFrame({'user_id': control_ids}), pd.DataFrame({'user_id': experimental_ids})
    
    def _get_student_data(self, df: pd.DataFrame, group: pd.DataFrame) -> pd.DataFrame:
        """Get complete data for a group of students."""
        return df[df['user_id'].isin(group['user_id'])]