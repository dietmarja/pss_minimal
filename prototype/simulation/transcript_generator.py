# File: prototype/simulation/transcript_generator.py

from datetime import datetime
from pathlib import Path
import json
from typing import List
import yaml

class TranscriptGenerator:
    """Generates meaningful transcripts showing learning progression."""
    
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
    def generate_transcript(self, session, topic: str) -> str:
        """Generate transcript with clear learning progression."""
        lines = [
            "================================================",
            "Mathematical Learning Session Transcript",
            "================================================",
            f"\nTopic: {topic}",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "Learning Progression Analysis:",
            "------------------------------------------------\n"
        ]
        
        # Track conceptual development
        current_level = None
        concepts_mastered = set()
        misconceptions_addressed = set()
        
        for event in session.events:
            # Add level transition markers
            if event.level != current_level:
                current_level = event.level
                lines.extend([
                    f"\n[{current_level.title()} Level Development]",
                    "------------------------------------------------\n"
                ])
            
            # Format timestamp
            timestamp = event.timestamp.strftime("%H:%M:%S")
            
            # Add detailed interaction with context
            lines.extend([
                f"[{timestamp}] {event.source.title()} Knowledge Source:",
                f"Context: {event.context.topic} (Difficulty: {event.context.difficulty:.2f})",
                f"Focus: {event.context.current_concept}\n",
                f"Q: {event.content}\n"
            ])
            
            if event.student_response:
                lines.extend([
                    "Student Response:",
                    f"{event.student_response}\n",
                    f"Understanding Gain: {event.understanding_depth:.2f}"
                ])
                
                # Track concept mastery
                if event.understanding_depth > 0.7:
                    concepts_mastered.add(event.context.current_concept)
                
                # Track addressed misconceptions
                if event.misconceptions_addressed:
                    misconceptions_addressed.update(event.misconceptions_addressed)
            
            lines.append("\n" + "-" * 48 + "\n")
        
        # Ad