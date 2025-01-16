# File: prototype/validation_setup.py

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, List, Any
import logging
from sklearn.model_selection import train_test_split
from scipy import stats
import json

logger = logging.getLogger(__name__)

def convert_to_serializable(obj: Any) -> Any:
    """Convert numpy types to Python native types for JSON serialization."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    return obj

class ValidationFramework:
    def __init__(self, ednet_path: str, output_dir: Path):
        self.ednet_path = ednet_path
        self.output_dir = output_dir
        self.data = None
        self.control_group = None
        self.experimental_group = None
    
    def setup_experiment(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Setup experimental validation."""
        logger.info("Setting up experimental validation")
        
        # Load EdNet Dataset
        self.data = pd.read_csv(self.ednet_path)
        logger.info(f"Loaded {len(self.data)} interactions from EdNet")
        
        # Create matched groups
        self.control_group, self.experimental_group = self._create_matched_groups()
        logger.info(f"Created matched groups with {len(self.control_group)} students each")
        
        return self.control_group, self.experimental_group
    
    def _create_matched_groups(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Create matched control and experimental groups."""
        # Calculate student statistics
        student_stats = (self.data.groupby('user_id')
                        .agg({
                            'correct': ['mean', 'count'],
                            'elapsed_time': 'mean'
                        }))
        
        # Reset index to make user_id a column
        student_stats = student_stats.reset_index()
        
        # Get proficiency scores with added noise to break ties
        proficiency = student_stats['correct']['mean'] + np.random.normal(0, 0.001, len(student_stats))
        
        # Create balanced split
        control, experimental = train_test_split(
            student_stats,
            test_size=0.5,
            random_state=42  # for reproducibility
        )
        
        return control, experimental
    
    def run_validation(self, pss_results: Dict, traditional_results: Dict) -> Dict:
        """Run validation analysis."""
        logger.info("Running validation analysis")
        
        # Calculate metrics
        metrics = self._compare_performance(pss_results, traditional_results)
        
        # Statistical analysis
        stats_results = self._statistical_analysis(
            pss_results.get('scores', []),
            traditional_results.get('scores', [])
        )
        
        # Effect sizes
        effect_sizes = self._calculate_effect_sizes(
            pss_results.get('scores', []),
            traditional_results.get('scores', [])
        )
        
        # Compile results and convert to serializable format
        validation_results = convert_to_serializable({
            'metrics': metrics,
            'statistical_analysis': stats_results,
            'effect_sizes': effect_sizes
        })
        
        # Save results
        self._save_results(validation_results)
        
        return validation_results
    
    def _compare_performance(self, pss_results: Dict, traditional_results: Dict) -> Dict:
        """Compare performance between groups."""
        metrics = {}
        
        for metric in ['scores', 'completion_rates', 'time_to_mastery']:
            pss_values = np.asarray(pss_results.get(metric, [0]))
            trad_values = np.asarray(traditional_results.get(metric, [0]))
            
            if pss_values.size > 0 and trad_values.size > 0:
                metrics[metric] = {
                    'pss_mean': float(np.mean(pss_values)),
                    'traditional_mean': float(np.mean(trad_values)),
                    'difference': float(np.mean(pss_values) - np.mean(trad_values))
                }
            else:
                metrics[metric] = {
                    'pss_mean': 0.0,
                    'traditional_mean': 0.0,
                    'difference': 0.0
                }
                
        return metrics
    
    def _statistical_analysis(self, pss_scores: List[float], traditional_scores: List[float]) -> Dict:
        """Conduct statistical analysis."""
        # Convert to numpy arrays
        pss_arr = np.asarray(pss_scores)
        trad_arr = np.asarray(traditional_scores)
        
        # Check if we have enough data
        if pss_arr.size == 0 or trad_arr.size == 0:
            return {
                't_statistic': 0.0,
                'p_value': 1.0,
                'significant': False
            }
        
        # Run t-test
        t_stat, p_value = stats.ttest_ind(pss_arr, trad_arr)
        
        return {
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            'significant': bool(p_value < 0.05)
        }
    
    def _calculate_effect_sizes(self, pss_scores: List[float], traditional_scores: List[float]) -> Dict:
        """Calculate effect sizes."""
        # Convert to numpy arrays
        pss_arr = np.asarray(pss_scores)
        trad_arr = np.asarray(traditional_scores)
        
        # Check if we have enough data
        if pss_arr.size == 0 or trad_arr.size == 0:
            return {
                'cohens_d': 0.0,
                'effect_magnitude': 'not calculable'
            }
        
        # Calculate pooled standard deviation
        pooled_std = np.sqrt((np.var(pss_arr) + np.var(trad_arr)) / 2)
        
        # Calculate Cohen's d
        if pooled_std == 0:
            d = 0.0
        else:
            d = float((np.mean(pss_arr) - np.mean(trad_arr)) / pooled_std)
        
        return {
            'cohens_d': d,
            'effect_magnitude': self._interpret_effect_size(d)
        }
    
    def _interpret_effect_size(self, d: float) -> str:
        """Interpret Cohen's d effect size."""
        if abs(d) < 0.2:
            return "negligible"
        elif abs(d) < 0.5:
            return "small"
        elif abs(d) < 0.8:
            return "medium"
        else:
            return "large"
    
    def _save_results(self, results: Dict) -> None:
        """Save validation results."""
        output_file = self.output_dir / 'validation_results.json'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved validation results to {output_file}")