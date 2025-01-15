# File: prototype/evaluation/emergent_evaluation.py

import torch
import logging
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from ..models.emergent_models import DynamicInteraction, EmergentPattern

logger = logging.getLogger(__name__)

class EmergentEvaluator:
    def __init__(self):
        self.ednet_patterns = []
        self.pss_patterns = []
        
    def evaluate_pss_session(self, session_data: List[DynamicInteraction]) -> Dict:
        """Evaluate PSS session patterns."""
        if not session_data:
            return self._create_empty_metrics()
            
        # Extract embeddings from interactions
        pattern_embeddings = [
            interaction.content_embedding for interaction in session_data
        ]
        
        # Create pattern from embeddings
        pss_pattern = self._create_pattern(pattern_embeddings)
        self.pss_patterns.append(pss_pattern)
        
        return {
            'pattern_similarity': self._calculate_pattern_similarity(pss_pattern),
            'learning_effectiveness': self._calculate_effectiveness(pss_pattern),
            'engagement_score': self._calculate_engagement(session_data),
            'temporal_alignment': self._calculate_temporal_alignment(session_data)
        }
    
    def _create_pattern(self, embeddings: List[torch.Tensor]) -> EmergentPattern:
        """Create pattern from embeddings."""
        if not embeddings:
            return EmergentPattern(
                embedding=torch.zeros(768),
                trajectory=[],
                success_rate=0.0,
                temporal_context=[]
            )
            
        # Stack embeddings and create mean representation
        stacked = torch.stack(embeddings)
        mean_embedding = torch.mean(stacked, dim=0)
        
        return EmergentPattern(
            embedding=mean_embedding,
            trajectory=embeddings,
            success_rate=self._calculate_success_rate(embeddings),
            temporal_context=[datetime.now() for _ in embeddings]  # Placeholder timestamps
        )
    
    def _calculate_pattern_similarity(self, pattern: EmergentPattern) -> float:
        """Calculate similarity with existing patterns."""
        if not self.ednet_patterns:
            return 0.5  # Default similarity when no comparison available
            
        similarities = []
        for ednet_pattern in self.ednet_patterns:
            sim = float(torch.cosine_similarity(
                pattern.embedding.unsqueeze(0),
                ednet_pattern.embedding.unsqueeze(0)
            ))
            similarities.append(sim)
            
        return float(np.mean(similarities))
    
    def _calculate_effectiveness(self, pattern: EmergentPattern) -> float:
        """Calculate effectiveness based on pattern evolution."""
        if not pattern.trajectory:
            return 0.0
            
        # Calculate trajectory improvement
        diffs = []
        for i in range(len(pattern.trajectory) - 1):
            diff = torch.norm(pattern.trajectory[i + 1] - pattern.trajectory[i])
            diffs.append(diff.item())
            
        if not diffs:
            return 0.5
            
        # Normalize improvements
        return float(np.mean(diffs))
    
    def _calculate_engagement(self, interactions: List[DynamicInteraction]) -> float:
        """Calculate engagement from interaction patterns."""
        if len(interactions) < 2:
            return 0.5
            
        # Calculate temporal density of interactions
        timestamps = [interaction.timestamp for interaction in interactions]
        time_diffs = [
            (t2 - t1).total_seconds() 
            for t1, t2 in zip(timestamps[:-1], timestamps[1:])
        ]
        
        # Convert to engagement score (inverse of average time difference)
        avg_time_diff = np.mean(time_diffs)
        return float(1.0 / (1.0 + avg_time_diff/60))  # Normalize to 0-1
    
    def _calculate_temporal_alignment(self, 
                                   interactions: List[DynamicInteraction]) -> float:
        """Calculate temporal pattern alignment."""
        if len(interactions) < 2:
            return 0.5
            
        # Extract pattern evolution
        embeddings = [i.content_embedding for i in interactions]
        
        # Calculate consistency of pattern changes
        changes = [
            torch.norm(e2 - e1).item() 
            for e1, e2 in zip(embeddings[:-1], embeddings[1:])
        ]
        
        return float(np.std(changes))  # Lower variation = better alignment
    
    def _calculate_success_rate(self, embeddings: List[torch.Tensor]) -> float:
        """Calculate success rate from pattern evolution."""
        if len(embeddings) < 2:
            return 0.5
            
        improvements = []
        for i in range(len(embeddings) - 1):
            diff = torch.norm(embeddings[i + 1] - embeddings[i])
            improvements.append(diff.item() > 0.1)  # Consider significant changes as improvements
            
        return float(np.mean(improvements))
    
    def _create_empty_metrics(self) -> Dict:
        """Create empty metrics dictionary."""
        return {
            'pattern_similarity': 0.0,
            'learning_effectiveness': 0.0,
            'engagement_score': 0.0,
            'temporal_alignment': 0.0
        }