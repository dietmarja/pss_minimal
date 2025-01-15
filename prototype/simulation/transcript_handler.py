# File: prototype/simulation/transcript_handler.py

from datetime import datetime
from pathlib import Path
from typing import List
from ..models.emergent_models import EmergentSession, DynamicInteraction

class TranscriptHandler:
    """Handles generation and saving of session transcripts."""
    
    @staticmethod
    def generate_transcript(session: EmergentSession) -> str:
        """Generate a readable transcript from session data."""
        transcript_lines = [
            f"PSS Session Transcript",
            f"Session ID: {session.id}",
            f"Date: {session.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n",
            "Interactions:\n"
        ]
        
        for interaction in session.interactions:
            timestamp = interaction.timestamp.strftime("%H:%M:%S")
            speaker = interaction.speaker.replace("_", " ").title()
            transcript_lines.append(
                f"[{timestamp}] {speaker}:\n"
                f"{interaction.content}\n"
                f"Topic: {interaction.topic}\n"
                f"Quality: {interaction.response_quality:.2f}\n"
            )
            
        return "\n".join(transcript_lines)
    
    @staticmethod
    def save_transcript(session: EmergentSession, output_dir: Path) -> Path:
        """Save session transcript to file."""
        # Ensure output directory exists
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = session.timestamp.strftime("%Y%m%d_%H%M%S")
        transcript_path = output_dir / f"session_transcript_{timestamp}.txt"
        
        # Generate and save transcript
        transcript = TranscriptHandler.generate_transcript(session)
        transcript_path.write_text(transcript)
        
        return transcript_path
