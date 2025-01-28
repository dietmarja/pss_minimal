# Persona Simulation System (PSS)

AI-driven teaching strategy evaluation system using EEDI dataset simulations.

## Key Features

- Dynamic teacher-student interaction simulation
- EEDI misconception data integration
- Four teaching approaches:
  - Socratic (dialectical questioning)
  - Constructivist (concept building)
  - Experiential (practical application)
  - Pattern-matching (baseline)
- A/B/C testing framework:
  - Pattern matching (base)
  - Persona-driven teaching
  - Control condition
- Statistical cross-validation

## Installation

```bash
python -m venv pss-env
source pss-env/bin/activate  # Windows: pss-env\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Basic validation:
```bash
python -m prototype.validation.run_validation \
    --data_path="prototype/data/eedi_processed.csv" \
    --n_folds=5
```

### Enhanced A/B/C testing:
```bash
python -m prototype.validation.run_validation \
    --data_path="prototype/data/eedi_processed.csv" \
    --n_folds=10 \
    --strategy="pattern|persona|control"
```

## Current Features

- Cross-validation with A/B/C testing
- Pattern matching vs persona comparison
- Statistical significance testing
- Teaching approach effectiveness metrics
- Interaction effects analysis

## Known Limitations

- Limited sample variation
- Basic pattern matching
- Simple persona implementation

## Next Steps

- Enhance persona sophistication
- Improve pattern matching baseline
- Add advanced statistical analysis
- Scale data utilization
