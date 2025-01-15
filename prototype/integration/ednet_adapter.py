# File: prototype/integration/ednet_adapter.py

import torch
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import logging

logger = logging.getLogger(__name__)

@dataclass
class EdNetInteraction:
    timestamp: datetime
    user_id: str
    question_id: str
    correct: bool
    response_time: float
    embedding: torch.Tensor
    topic: str
    concept_embeddings: torch.Tensor

class EdNetAdapter:
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = None  # Will be initialized after seeing the data
        self.concept_embeddings = {}
        self.topic_vectors = {}
        self.interaction_patterns = []
    
    def process_interactions(self, df: pd.DataFrame) -> List[EdNetInteraction]:
        """Convert EdNet data to interaction format with embeddings."""
        logger.info("Processing interactions...")
        
        # Create feature matrix for embedding
        feature_matrix = self._create_feature_matrix(df)
        
        # Initialize PCA based on data dimensions
        n_features = feature_matrix.shape[1]
        n_components = min(n_features - 1, 10)  # Use at most 10 components
        self.pca = PCA(n_components=n_components)
        
        # Scale features
        scaled_features = self.scaler.fit_transform(feature_matrix)
        
        # Reduce dimensionality
        reduced_features = self.pca.fit_transform(scaled_features)
        logger.info(f"Reduced features from {n_features} to {n_components} dimensions")
        
        # Create embeddings
        interactions = []
        for i, row in df.iterrows():
            interaction = self._create_interaction(row, reduced_features[i])
            interactions.append(interaction)
            self.interaction_patterns.append(interaction)
        
        logger.info(f"Processed {len(interactions)} interactions")
        return interactions

    def _create_feature_matrix(self, df: pd.DataFrame) -> np.ndarray:
        """Create feature matrix for embedding."""
        # Extract numerical features
        features = [
            df['correct'].astype(float),
            df['response_time'].fillna(0)
        ]
        
        # Add topic encoding
        topic_dummies = pd.get_dummies(df['topic'], prefix='topic')
        features.extend([topic_dummies[col] for col in topic_dummies.columns])
        
        return np.column_stack(features)

    def _create_interaction(self, row: pd.Series, reduced_features: np.ndarray) -> EdNetInteraction:
        """Create single interaction with embeddings."""
        return EdNetInteraction(
            timestamp=row['timestamp'],
            user_id=row['user_id'],
            question_id=str(row['question_id']),
            correct=bool(row['correct']),
            response_time=float(row['response_time']) if pd.notna(row['response_time']) else 0.0,
            embedding=torch.tensor(reduced_features, dtype=torch.float32),
            topic=str(row['topic']),
            concept_embeddings=torch.tensor(reduced_features, dtype=torch.float32)
        )

    def load_ednet_data(self, filepath: str) -> pd.DataFrame:
        """Load and preprocess EdNet data."""
        logger.info(f"Loading EdNet data from {filepath}")
        df = pd.read_csv(filepath)
        
        # Convert timestamps
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        logger.info(f"Loaded {len(df)} interactions")
        return df