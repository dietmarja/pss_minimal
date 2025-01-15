# File: prototype/models/emergent_models.py

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np

@dataclass
class DynamicInteraction:
    """Represents a single interaction in the system."""
    timestamp: datetime
    speaker: str
    content: str
    topic: str
    interaction_type: str
    response_quality: float
    state_vector: Optional[np.ndarray] = None
    
    def __post_init__(self):
        if self.state_vector is None:
            # Simple 3D state vector: [engagement, understanding, complexity]
            self.state_vector = np.random.rand(3)

@dataclass
class EmergentSession:
    """Represents a complete teaching session."""
    id: str
    timestamp: datetime
    interactions: List[DynamicInteraction] = field(default_factory=list)
    state_trace: List[np.ndarray] = field(default_factory=list)
    
    def add_interaction(self, interaction: DynamicInteraction) -> None:
        """Add an interaction and update session state."""
        self.interactions.append(interaction)
        # Update state trace with the interaction's state vector
        if interaction.state_vector is not None:
            self.state_trace.append(interaction.state_vector.copy())
    
    def get_session_metrics(self) -> Dict:
        """Calculate basic session metrics."""
        if not self.interactions:
            return {
                "num_interactions": 0,
                "avg_quality": 0.0,
                "engagement_level": 0.0
            }
        
        qualities = [i.response_quality for i in self.interactions]
        return {
            "num_interactions": len(self.interactions),
            "avg_quality": float(np.mean(qualities)),
            "engagement_level": float(np.mean(qualities) * len(self.interactions) / 10)
        }