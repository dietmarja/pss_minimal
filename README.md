# Persona Simulation System (PSS)


## Overview
PSS implements an AI-first approach to teaching simulation and curriculum design, moving beyond traditional rule-based systems to enable emergent, dynamic learning experiences.

## Core Architecture
The system implements a purely AI-first approach with the following key components:

### Knowledge Space
- Dynamic concept representation using transformer-based embeddings
- Real-time relationship mapping between topics
- Adaptive concept difficulty assessment
- Emergent learning progression paths
- No predefined rules or static relationships

### Models
Core data structures and state representations:
```python
# From models.py
@dataclass
class Persona:
    id: str
    expertise: str  # beginner/intermediate/advanced
    engagement_level: float  # 0-1 scale
    learning_style: str
    participation_rate: float = 0.0
    understanding: Dict[str, float] = field(default_factory=dict)

@dataclass
class Interaction:
    timestamp: datetime
    speaker: str
    content: str
    topic: str
    interaction_type: str
    response_quality: float = 0.0
```

### Simulation Engine
The simulation engine orchestrates dynamic interactions:
```python
# From simulation.py
class TeachingSimulation:
    def __init__(self, config_path: str):
        self.state_manager = StateEvolutionManager()
        self.content_generator = ContentGenerator()
        self.interaction_manager = InteractionManager()

    def run_session(self) -> Session:
        """Run complete teaching session with emergent interactions."""
```

### State Evolution
Dynamic state management and evolution:
```python
# From state_evolution.py
class StateEvolutionManager:
    """Manages dynamic learning states."""
    def update_state(self, persona_id: str, interaction: dict) -> None:
        # Dynamic state updates based on interactions
```

### Content Generation
AI-driven content generation system:
```python
# From content_generation.py
class ContentGenerator:
    """Generates contextual content."""
    def __init__(self):
        self.generator = pipeline('text-generation', model='gpt2')

    def generate_content(self, context: ContentContext) -> str:
        # Context-aware content generation
```

## Installation and Requirements

### Dependencies
Required Python packages:
```bash
# Core dependencies
numpy>=1.19.2
pandas>=1.2.0
torch>=1.8.0  # Required for embeddings
transformers>=4.5.0  # For content generation
scikit-learn>=0.24.0  # For validation metrics
networkx>=2.5  # For interaction analysis
matplotlib>=3.3.0  # For visualizations
streamlit>=0.85.0  # For dashboard

# Additional requirements
plotly>=4.14.0  # Interactive visualizations
scipy>=1.6.0  # Statistical analysis
pyyaml>=5.4.0  # Configuration management
```

### Installation Steps
Complete setup process:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Environment Configuration
Required environment setup:
```bash
# Set required environment variables
export PYTHONPATH="${PYTHONPATH}:./prototype"
export TRANSFORMERS_OFFLINE=1  # Optional: offline mode
```

## Project Structure
Current implementation structure:
```bash
prototype/
├── __init__.py
├── models.py              # Core data structures
├── simulation.py          # Main simulation engine
├── content_generation.py  # AI content generation
├── state_evolution.py     # Dynamic state management
├── validation.py          # Validation metrics
├── config_generator.py    # Dynamic config generation
└── visualization/
    └── learning_visualizer.py

config/
├── templates/            # Configuration templates
└── subjects/            # Subject-specific configs

results/
└── <timestamp>/         # Session results
    ├── config.json      # Session configuration
    ├── metrics.json     # Validation metrics
    ├── report.md        # Human-readable report
    └── visualizations/  # Generated plots
```

Each component serves a specific purpose in the AI-first architecture:
- `models.py`: Core data structures for personas and interactions
- `simulation.py`: Main simulation engine orchestrating the system
- `content_generation.py`: AI-driven content generation
- `state_evolution.py`: Dynamic state tracking and evolution
- `validation.py`: Comprehensive validation metrics
- `config_generator.py`: Dynamic configuration generation

## Running the Prototype

### Basic Usage
Run the prototype with various configurations:
```bash
# Basic run with default settings
python run_prototype.py

# Specify number of students
python run_prototype.py --num_students 15

# Multiple sessions with custom output
python run_prototype.py --num_students 10 \
                       --num_sessions 5 \
                       --output custom_results
```

### Command Line Arguments
Available options:
- `--num_students`: Number of students to simulate (default: 10)
- `--num_sessions`: Number of teaching sessions (default: 3)
- `--output`: Output directory for results (default: "results")
- `--config`: Custom configuration file path

### Output Structure
Results are organized in timestamped directories:
```bash
results/
└── 20250113_123456/    # Timestamp
    ├── config.json     # Generated configuration
    ├── metrics.json    # Validation metrics
    ├── report.md       # Human-readable report
    └── visualizations/ # Generated plots
        ├── learning_progression.png
        └── general_metrics.png
```

## Blackboard Architecture Implementation

### Core Components
The blackboard architecture implements a shared knowledge space with multiple specialized knowledge sources:
```python
class BlackboardSystem:
    def __init__(self):
        self.knowledge_sources = {
            'socratic': KnowledgeSource(
                expertise=['questioning', 'critical_thinking'],
                confidence=0.8
            ),
            'constructivist': KnowledgeSource(
                expertise=['knowledge_building', 'scaffolding'],
                confidence=0.7
            ),
            'experiential': KnowledgeSource(
                expertise=['practical_application', 'reflection'],
                confidence=0.75
            )
        }
```

### Knowledge Levels
The system maintains four distinct levels of understanding:
- **Observation Level**: Raw educational interactions and responses
- **Pattern Level**: Emerging patterns in learning dynamics
- **Concept Level**: Consolidated understanding of educational concepts
- **Principle Level**: Higher-order pedagogical principles

### Hypothesis Management
Each knowledge level maintains and evaluates hypotheses:
```python
@dataclass
class Hypothesis:
    content: str
    confidence: float
    supporting_sources: Set[str]
    timestamp: datetime
    embedding: np.ndarray
```

### Confidence Computation
Hypothesis confidence is computed through source reliability:
```python
def _update_level_confidence(self, level: str):
    confidences = []
    for hypothesis in self.levels[level].hypotheses:
        source_confidence = np.mean([
            self.knowledge_sources[source].confidence
            for source in hypothesis.supporting_sources
        ])
        confidences.append(
            hypothesis.confidence * source_confidence
        )
```

### Integration Points
Key integration points for extending the system:
- `add_hypothesis()`: Add new educational insights
- `get_current_understanding()`: Query system state
- `generate_interaction()`: Create pedagogical interactions

### Technical Requirements
Dependencies and computational requirements:
```yaml
dependencies:
  numpy: ">=1.24.3"
  pandas: ">=1.5.3"
  scikit-learn: ">=0.24.0"

memory:
  minimum: "4GB"
  recommended: "8GB"
```

## Validation Methods

### Metrics Framework
The system implements comprehensive validation metrics:
- **Interaction Coherence**
  - Measures natural flow of discussions
  - Analyzes topic progression
  - Evaluates response relevance
- **Learning Effectiveness**
  - Tracks understanding progression
  - Measures concept mastery
  - Analyzes learning trajectories
- **Engagement Analysis**
  - Participation patterns
  - Discussion quality
  - Peer interaction rates

### Validation Process
Automated validation workflow:
```python
# Validation process
validator = EnhancedValidationMetrics(simulation)
metrics = validator.calculate_all_metrics()

# Available metrics
{
    'interaction_coherence': float,  # 0-1 scale
    'learning_effectiveness': Dict[str, float],
    'persona_adaptation': float,
    'engagement_balance': float,
    'topic_coverage': float,
    'discussion_depth': float
}
```

### Interpretation Guidelines
Metric interpretation ranges:
- 0.8-1.0: Excellent
- 0.6-0.8: Good
- 0.4-0.6: Moderate
- <0.4: Needs improvement

## Debugging and Common Issues

### Common Issues
Frequently encountered issues and solutions:
- **Missing Dependencies**
  - Issue: "No module named 'torch'"
  - Solution: Install PyTorch: `pip install torch`
- **Configuration Errors**
  - Issue: Invalid persona configurations
  - Solution: Use `config_generator` to create valid configs
- **Memory Issues**
  - Issue: Out of memory with large simulations
  - Solution: Reduce batch size or number of students

### Debugging Tools
Available debugging utilities:
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with detailed output
python run_prototype.py --verbose

# Analyze specific session
python -m prototype.debug analyze_session results/20250113_123456/
```

### Performance Optimization
Optimization guidelines:
- Use appropriate batch sizes for content generation
- Enable caching for embeddings
- Optimize number of interactions per session
- Monitor memory usage with large simulations

## AI-First Empirical Evaluation
The system implements an emergence-based evaluation approach that learns and adapts from real-world educational data.

### Project Structure
Core evaluation components:
```bash
prototype/
├── evaluation/
│   ├── emergent_evaluation.py  # Core evaluation engine
│   └── pattern_extraction.py   # Pattern discovery
├── integration/
│   └── ednet_adapter.py       # EdNet data integration
└── visualization/
    └── eval_visualizer.py     # Dynamic visualizations
```

### EdNet Integration
The evaluation leverages the EdNet-KT1 dataset through dynamic pattern discovery:
- **Dynamic Concept Mapping**
  - Automatic discovery of concept relationships
  - Embedding-based similarity analysis
  - Adaptive concept space evolution
- **Pattern Extraction**
  - Learning trajectory analysis
  - Temporal pattern discovery
  - Success pattern identification
- **Adaptive Integration**
  - Real-time format conversion
  - Dynamic feature extraction
  - Continuous pattern updating

### Emergent Evaluation Framework
The evaluation process implements an AI-first approach:
```python
# From emergent_evaluation.py
class EmergentEvaluator:
    def evaluate_session(self):
        """Discover and evaluate patterns."""
        # Extract learning patterns
        # Compare with EdNet patterns
        # Calculate emergence-based metrics
```

### Pattern-Based Metrics
The system discovers and evolves metrics through pattern analysis:
- **Learning Patterns**
  - Trajectory embeddings
  - Success pattern matching
  - Temporal alignment
- **Engagement Analysis**
  - Interaction density
  - Response patterns
  - Temporal engagement curves
- **Effectiveness Measures**
  - Pattern similarity scores
  - Learning effectiveness
  - Temporal efficiency

### Integration with PSS
The evaluation framework integrates with the core PSS system:
- **Pattern Discovery**
  - Extracts patterns from PSS sessions
  - Compares with EdNet patterns
  - Evolves teaching strategies
- **Dynamic Adaptation**
  - Updates concept mappings
  - Evolves evaluation metrics
  - Adapts to new patterns

### Running Evaluation
Execute with dynamic pattern discovery:
```bash
python run_prototype.py --ednet_data path/to/ednet_kt1.csv --enable_patterns
```

Available options:
- `--ednet_data`: Path to EdNet dataset
- `--enable_patterns`: Enable pattern discovery
- `--pattern_threshold`: Pattern similarity threshold
- `--adaptation_rate`: Pattern adaptation rate

### Visualization
The system generates dynamic visualizations:
```bash
results/
└── evaluation/
    ├── pattern_evolution.png  # Pattern development
    ├── learning_curves.png    # Comparative learning
    └── engagement_map.png     # Engagement patterns
```

### Interpretation Framework
Pattern-based interpretation guidelines:
- **Pattern Similarity**
  - >0.8: Strong pattern match
  - 0.6-0.8: Moderate alignment
  - <0.6: Weak pattern match
- **Learning Effectiveness**
  - Based on pattern evolution
  - Weighted by success rates
  - Temporal efficiency factor
- **Engagement Quality**
  - Pattern density analysis
  - Temporal engagement curves
  - Interaction rhythm patterns

This AI-first evaluation framework provides dynamic validation of the PSS system's effectiveness through emergent pattern discovery and comparison with real-world educational data. The approach allows for continuous adaptation and evolution of both the evaluation metrics and the teaching strategies.

## To Do
There are several gaps in the implementation.

### Missing bar in general_metrics.png
The issue is that we're filtering metrics incorrectly. We need to modify the visualization code to properly handle small values like `persona_adaptation` (0.002).

### Actual curriculum design (partially done!)
We're currently simulating interactions but not actually designing the curriculum. We need to:
- Extract patterns from successful interactions
- Identify optimal topic sequences
- Generate curriculum recommendations based on interaction analysis
- Produce specific curriculum design outputs

### Evaluation results
While we have metrics, we don't have:
- Detailed analysis of learning patterns
- Curriculum effectiveness evaluation
- Recommendations for improvements
- Comparison with curriculum design goals

### Transcript (partially done)
We're generating interactions but not saving them in a readable format. We already have added the method `save_transcript` to `simulation.py`. But it does not seem to produce a transcript.

## Misc
**Code Presentation**. When you return code, make sure that:
- Each code box has a path and file name (commented out) in line 1
- The download link offers the EXACT name of the file to be downloaded. For instance, give me "run_minimal.py" and not "run-minimal.py".
- Never hard code what could vary, e.g., code must be content-agnostic — do not mix code and content and do not hard code the number of students

**Do what Reviewers like.**
A previous version of the paper received this review:
"The experimental validation relies heavily on simulated personas without real-world validation. The statistical analysis lacks proper control groups and baseline comparisons, and the improvement score metrics require more rigorous validation."
This time we have to avoid those issues.

## Reminder
Always maintain an AI-first approach. So do not drift into scripted interactions or into piling up methods.
