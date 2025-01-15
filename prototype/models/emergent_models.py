# File: prototype/models/emergent_models.py

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime
import numpy as np

@dataclass
class DynamicInteraction:
    """Represents an interaction with emergent dynamics."""
    timestamp: datetime
    embedding: np.ndarray
    quality: float
    patterns: List[Dict] = field(default_factory=list)

@dataclass
class EmergentPattern:
    """Represents an emergent pattern in the concept space."""
    embedding: np.ndarray
    strength: float
    coherence: float
    timestamp: datetime = field(default_factory=datetime.now)
    related_patterns: Set[int] = field(default_factory=set)
    
    def evolve(self, influence: np.ndarray, learning_rate: float = 0.1) -> None:
        """Evolve pattern based on new influence."""
        self.embedding = np.tanh(
            self.embedding + learning_rate * influence
        )
        
    def similarity(self, other: 'EmergentPattern') -> float:
        """Compute similarity with another pattern."""
        return float(np.dot(
            self.embedding / np.linalg.norm(self.embedding),
            other.embedding / np.linalg.norm(other.embedding)
        ))

@dataclass
class DynamicState:
    """Represents the dynamic state of the learning system."""
    timestamp: datetime
    embedding: np.ndarray
    active_patterns: List[EmergentPattern]
    stability: float = 0.0
    
    @property
    def complexity(self) -> float:
        """Measure state complexity through pattern interactions."""
        if not self.active_patterns:
            return 0.0
        n = len(self.active_patterns)
        interactions = np.zeros((n, n))
        for i, p1 in enumerate(self.active_patterns):
            for j, p2 in enumerate(self.active_patterns):
                if i != j:
                    interactions[i,j] = p1.similarity(p2)
        return float(np.mean(np.abs(interactions)))

@dataclass
class EmergentSession:
    """Represents a complete learning session with emergent dynamics."""
    id: str
    timestamp: datetime
    interactions: List[DynamicInteraction] = field(default_factory=list)
    state_history: List[DynamicState] = field(default_factory=list)
    pattern_evolution: Dict[int, List[EmergentPattern]] = field(default_factory=dict)
    
    def add_interaction(self, interaction: DynamicInteraction) -> None:
        """Add new interaction and update state."""
        self.interactions.append(interaction)
        state = self._compute_state(interaction)
        self.state_history.append(state)
        self._update_patterns(state)
    
    def _compute_state(self, interaction: DynamicInteraction) -> DynamicState:
        """Compute new state from interaction."""
        return DynamicState(
            timestamp=interaction.timestamp,
            embedding=interaction.embedding,
            active_patterns=self._extract_active_patterns(interaction)
        )
    
    def _extract_active_patterns(self, 
                               interaction: DynamicInteraction) -> List[EmergentPattern]:
        """Extract active patterns from interaction."""
        patterns = []
        for p in interaction.patterns:
            pattern = EmergentPattern(
                embedding=p['embedding'],
                strength=p['strength'],
                coherence=p['coherence']
            )
            patterns.append(pattern)
        return patterns
    
    def _update_patterns(self, state: DynamicState) -> None:
        """Update pattern evolution."""
        for pattern in state.active_patterns:
            pattern_id = hash(pattern.embedding.tobytes())
            if pattern_id not in self.pattern_evolution:
                self.pattern_evolution[pattern_id] = []
            self.pattern_evolution[pattern_id].append(pattern)
    
    def get_session_metrics(self) -> Dict:
        """Calculate session metrics from emergent patterns."""
        if not self.interactions:
            return {
                "num_interactions": 0,
                "avg_quality": 0.0,
                "complexity": 0.0
            }
        
        qualities = [i.quality for i in self.interactions]
        complexities = [s.complexity for s in self.state_history]
        
        return {
            "num_interactions": len(self.interactions),
            "avg_quality": float(np.mean(qualities)),
            "complexity": float(np.mean(complexities))
        }