# File: prototype/models/emergent_models.py

import torch
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class DynamicState:
    embeddings: torch.Tensor
    temporal_patterns: List[torch.Tensor] = field(default_factory=list)
    interaction_history: List[Dict] = field(default_factory=list)

@dataclass
class EmergentPattern:
    """Pattern representation for learning trajectory."""
    embedding: torch.Tensor
    trajectory: List[torch.Tensor]
    success_rate: float
    temporal_context: List[datetime]

@dataclass
class DynamicInteraction:
    timestamp: datetime
    content_embedding: torch.Tensor
    context_state: DynamicState
    evolution_trace: List[torch.Tensor]
    speaker: str
    content: str = ""
    topic: str = ""
    interaction_type: str = "pattern"
    response_quality: float = 0.0

@dataclass
class EmergentSession:
    id: str
    timestamp: datetime
    state_trace: List[torch.Tensor] = field(default_factory=list)
    interaction_embeddings: List[torch.Tensor] = field(default_factory=list)
    interactions: List[DynamicInteraction] = field(default_factory=list)

    def add_interaction(self, interaction: DynamicInteraction) -> None:
        """Add interaction and update session state."""
        self.interactions.append(interaction)
        self.interaction_embeddings.append(interaction.content_embedding)
        new_state = self._compute_state()
        self.state_trace.append(new_state)

    def _compute_state(self) -> torch.Tensor:
        """Compute current session state from interactions."""
        if not self.interaction_embeddings:
            return torch.zeros(768)  # Default BERT dimension
        return torch.stack(self.interaction_embeddings).mean(dim=0)

    @property
    def current_state(self) -> torch.Tensor:
        """Get current session state."""
        if not self.state_trace:
            return torch.zeros(768)
        return self.state_trace[-1]