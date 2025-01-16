# File: prototype/simulation/transcript_generator.py

from typing import List
from datetime import datetime, timedelta
from pathlib import Path
from .educational_discourse import DiscourseContribution
import logging

logger = logging.getLogger(__name__)

class TranscriptGenerator:
    """Generates readable transcripts from educational discourse."""
    
    @staticmethod
    def save_transcript(contributions: List[DiscourseContribution], 
                       topic: str,
                       output_path: Path) -> None:
        """Generate and save a readable transcript."""
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Format header
        lines = [
            "=" * 80,
            "Educational Discussion Transcript",
            "=" * 80,
            f"\nTopic: {topic.title()}",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\nDiscussion Evolution:",
            "-" * 80 + "\n"
        ]
        
        # Track discussion phases
        current_phase = None
        current_time = datetime.now()
        
        for contribution in contributions:
            # Update phase headers
            if contribution.level != current_phase:
                current_phase = contribution.level
                lines.extend([
                    f"\n[Phase: {current_phase.title()}]",
                    "-" * 40 + "\n"
                ])
            
            # Add realistic timing with proper increment
            current_time = current_time + timedelta(seconds=45)
            
            # Format contribution with indentation for readability
            lines.extend([
                f"[{current_time.strftime('%H:%M:%S')}] {contribution.speaker}:",
                f"    {contribution.content}\n"
            ])
            
            # Add context notes if significant contribution
            if contribution.confidence > 0.7:
                lines.append(f"    (Key insight at {contribution.level} level)\n")
        
        # Add discussion analysis
        lines.extend([
            "\n" + "=" * 80,
            "Discussion Analysis",
            "=" * 80 + "\n",
            "Understanding Progression:",
            "-" * 40
        ])
        
        # Analyze level progression
        level_progression = {}
        for c in contributions:
            if c.level not in level_progression:
                level_progression[c.level] = 0
            level_progression[c.level] += 1
        
        for level, count in level_progression.items():
            lines.append(f"\n{level.title()} Level:")
            lines.append(f"  - {count} contributions")
            lines.append(f"  - Depth: {'High' if count > 3 else 'Moderate' if count > 1 else 'Initial'}")
        
        lines.extend([
            "\nParticipation Analysis:",
            "-" * 40
        ])
        
        # Analyze participation
        speakers = {}
        for c in contributions:
            if c.speaker not in speakers:
                speakers[c.speaker] = 0
            speakers[c.speaker] += 1
            
        for speaker, count in speakers.items():
            lines.append(f"\n{speaker}:")
            lines.append(f"  - {count} contributions")
            lines.append(f"  - Engagement: {'High' if count > 3 else 'Moderate' if count > 1 else 'Limited'}")
        
        # Save transcript
        with open(output_path / 'session_transcript.txt', 'w') as f:
            f.write('\n'.join(lines))
            
        logger.info(f"Saved transcript to {output_path / 'session_transcript.txt'}")