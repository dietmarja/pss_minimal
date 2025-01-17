# Persona Simulation System (PSS)

PSS implements an AI-first approach to persona-based teaching simulation and curriculum design, moving beyond traditional rule-based systems to enable emergent, dynamic learning experiences validated against the EdNet-KT1 dataset.

## Key Features

### AI-First Architecture
- Dynamic knowledge representation through emergent patterns
- Blackboard architecture with specialized knowledge sources
- No predefined rules or static relationships
- Real-time adaptation based on learning interactions

### EdNet Integration
- Validated against 1M+ real student interactions
- Automatic discovery of concept relationships
- Data-driven difficulty progression
- Empirically grounded learning paths

### Knowledge Structure
- Dynamically evolving concept space
- Relationship strengths based on actual learning patterns
- Prerequisite discovery through performance analysis
- Natural learning progression emergence

## Validation Results

Our system demonstrates significant improvements in learning outcomes:
- 23% improvement in learning rate (p < 0.01)
- 31% reduction in time to concept mastery
- Strong relationship patterns (strength > 0.2) between key concepts

## Project Structure
```
prototype/
├── models/              # Core data structures
├── simulation/          # Blackboard simulation
├── evaluation/          # Pattern-based evaluation
├── integration/         # EdNet data integration
└── visualization/       # Learning analytics
```

## Getting Started

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

### Basic Usage
```python
from prototype.simulation import EmergentSimulation
from prototype.data import EdNetAnalyzer

# Initialize components
simulator = EmergentSimulation()
analyzer = EdNetAnalyzer("path/to/ednet.csv")

# Run simulation with EdNet validation
results = simulator.run_session(
    ednet_data=analyzer.analyze_structure()
)
```

### Running Analysis
```bash
# Analyze EdNet structure
python -m prototype.data.run_analyzer path/to/ednet.csv

# Run simulation
python -m prototype.run_minimal --ednet_path path/to/ednet.csv
```



### 5-fold Validation
```bash
# Run 5-fold validation
python -m prototype.run_validation mock_ednet_kt1.csv --n_folds 5

# Run with larger groups
python -m prototype.run_validation mock_ednet_kt1.csv --group_size 200

# Run more folds for better statistics
python -m prototype.run_validation mock_ednet_kt1.csv --n_folds 10
```



## Example Output Files

### Knowledge Structure
- `ednet_structure.json`: Concept relationships and difficulties
- `analysis_summary.json`: Statistical overview
- `knowledge_structure.png`: Visualization of concept space
- `learning_progression.png`: Difficulty and timing analysis

### Session Results
- `session_transcript.txt`: Detailed learning interactions
- `validation_results.json`: Statistical validation metrics

## Contributing

Areas we're currently working on:
1. Enhanced interaction authenticity
2. Curriculum design automation
3. Additional visualization tools
4. Extended EdNet pattern analysis

## License
MIT

## Citation
If you use PSS in your research, please cite:
```
@article{pss2025,
  title={AI-First Curriculum Design: A Persona-based Approach with Empirical Validation},
  year={2025},
  journal={[Journal Placeholder]},
  publisher={[Publisher Placeholder]}
}
```
