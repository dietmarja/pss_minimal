# File: prototype/models/emergent_models.py

import torch
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class DynamicState:
    """Emergent learning state representation"""
    embeddings: torch.Tensor
    temporal_patterns: List[torch.Tensor] = field(default_factory=list)
    interaction_history: List[Dict] = field(default_factory=list)

@dataclass
class EmergentPattern:
    """Pattern representation for learning trajectory"""
    embedding: torch.Tensor
    trajectory: List[torch.Tensor]
    success_rate: float
    temporal_context: List[datetime]

@dataclass
class EmergentPersona:
    """Dynamic persona representation"""
    id: str
    state: DynamicState
    knowledge_embeddings: torch.Tensor
    interaction_patterns: torch.Tensor

@dataclass
class DynamicInteraction:
    """Self-evolving interaction representation"""
    timestamp: datetime
    content_embedding: torch.Tensor
    context_state: DynamicState
    evolution_trace: List[torch.Tensor]
    speaker: str
    content: str
    topic: str
    interaction_type: str
    response_quality: float = 0.0

@dataclass
class EmergentSession:
    """Dynamic session representation"""
    id: str
    timestamp: datetime
    state_trace: List[torch.Tensor] = field(default_factory=list)
    interaction_embeddings: List[torch.Tensor] = field(default_factory=list)
    interactions: List[DynamicInteraction] = field(default_factory=list)
    
    def add_interaction(self, interaction: DynamicInteraction) -> None:
        """Add interaction to session"""
        self.interactions.append(interaction)
        self.interaction_embeddings.append(interaction.content_embedding)
        self.state_trace.append(self._compute_state())
    
    def _compute_state(self) -> torch.Tensor:
        """Compute emergent session state"""
        if not self.interaction_embeddings:
            return torch.zeros(768)  # BERT hidden size
        return torch.stack(self.interaction_embeddings).mean(dim=0)