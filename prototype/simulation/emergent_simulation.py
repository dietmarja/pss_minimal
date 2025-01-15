# File: prototype/simulation/emergent_simulation.py

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import random
import numpy as np
from prototype.models.emergent_models import DynamicInteraction, EmergentSession

class EmergentSimulation:
    def __init__(self):
        self.roles = ["professor", "student_1", "student_2", "student_3"]
        self.discourse_state = {"depth": 0, "engagement": 0.5}
        
    def run_session(self, topics: Optional[List[str]] = None) -> EmergentSession:
        """Run a complete teaching session."""
        if topics is None:
            topics = ["general"]
            
        session = EmergentSession(
            id=str(datetime.now().timestamp()),
            timestamp=datetime.now()
        )
        
        # Professor starts the discussion
        interaction = self._generate_interaction(
            "professor",
            interaction_type="introduction",
            topic=topics[0]
        )
        session.add_interaction(interaction)
        
        # Natural discussion emerges
        for i in range(4):
            # Update discourse state
            self.discourse_state["depth"] += 0.2
            self.discourse_state["engagement"] = min(1.0, 
                self.discourse_state["engagement"] + 0.15)
            
            # Select topic
            topic_idx = min(i // 2, len(topics) - 1)
            current_topic = topics[topic_idx]
            
            # Generate student response
            student_id = f"student_{i + 1}"
            interaction = self._generate_interaction(
                student_id,
                interaction_type="response",
                topic=current_topic
            )
            session.add_interaction(interaction)
        
        return session
    
    def _generate_interaction(self, 
                            speaker: str, 
                            interaction_type: str,
                            topic: str) -> DynamicInteraction:
        """Generate a meaningful interaction."""
        if speaker == "professor":
            if interaction_type == "introduction":
                content = self._generate_professor_intro()
            else:
                content = self._generate_professor_response()
        else:
            content = self._generate_student_response()
            
        # Generate state vector [engagement, understanding, complexity]
        state_vector = np.array([
            self.discourse_state["engagement"],
            min(1.0, self.discourse_state["depth"] + random.random() * 0.2),
            random.random() * self.discourse_state["depth"]
        ])
        
        quality = self._calculate_quality()
            
        return DynamicInteraction(
            timestamp=self._generate_timestamp(),
            speaker=speaker,
            content=content,
            topic=topic,
            interaction_type=interaction_type,
            response_quality=quality,
            state_vector=state_vector
        )
    
    def _generate_professor_intro(self) -> str:
        intros = [
            "How do different learning approaches affect understanding?",
            "What makes some explanations more effective than others?",
            "Let's explore how we build knowledge together.",
            "What patterns have you noticed in your learning process?"
        ]
        return random.choice(intros)
        
    def _generate_student_response(self) -> str:
        depth = self.discourse_state["depth"]
        if depth < 0.3:
            responses = [
                "I think it depends on the individual learner.",
                "Different methods work for different people.",
                "Sometimes simpler explanations are better."
            ]
        else:
            responses = [
                "I've noticed that connecting concepts helps me learn better.",
                "When we discuss ideas, new patterns become clear.",
                "The most effective learning often emerges from discussion."
            ]
        return random.choice(responses)

    def _generate_professor_response(self) -> str:
        responses = [
            "That's an interesting perspective. Can you elaborate?",
            "How does that connect to your learning experience?",
            "What specific examples come to mind?",
            "How might this apply in different contexts?"
        ]
        return random.choice(responses)
        
    def _calculate_quality(self) -> float:
        base_quality = 0.6
        depth_factor = self.discourse_state["depth"] * 0.2
        engagement_factor = self.discourse_state["engagement"] * 0.2
        quality = base_quality + depth_factor + engagement_factor
        return min(1.0, quality)
        
    def _generate_timestamp(self) -> datetime:
        last_time = getattr(self, 'last_time', datetime.now())
        delay = random.uniform(15, 30)
        new_time = last_time + timedelta(seconds=delay)
        self.last_time = new_time
        return new_time