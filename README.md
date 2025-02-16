# Persona Simulation System (PSS)
AI-driven teaching strategy evaluation system for analyzing and improving mathematical misconception remediation through the EEDI dataset.

## Project Overview
PSS combines case-based reasoning (CBR) with AI teaching personas to evaluate different teaching strategies in reducing mathematical misconceptions. Using 17 million student interactions from the EEDI dataset, the system provides empirically-grounded insights into teaching effectiveness.

## Key Features
### Teaching Strategies
Five distinct teaching approaches are implemented:
- Socratic: Dialectical questioning to stimulate critical thinking
- Constructive: Scaffolded concept building
- Experiential: Practical application and real-world context
- Rule-based: Systematic pattern-based instruction
- Traditional: Baseline comparison approach

### Analysis Framework
- Hybrid system combining CBR and AI approaches
- Comprehensive cross-validation system
- Statistical significance testing
- Interaction pattern analysis
- Performance comparison across approaches

### Data Integration
- EEDI dataset integration (17M student interactions)
- Misconception pattern analysis
- Teaching strategy effectiveness tracking
- Student response modeling

## Implementation

### Prerequisites
- Python 3.8+
- Virtual environment capability
- Minimum 16GB RAM recommended

### Installation
```bash
# Create virtual environment
python -m venv pss-env

# Activate environment
source pss-env/bin/activate  # Windows: pss-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
