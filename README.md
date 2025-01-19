# Persona Simulation System (PSS)

An AI-first approach to teaching strategy evaluation using simulated teacher-student interactions based on the EEDI dataset.

## Overview

PSS transforms static EEDI misconception data into dynamic teaching simulations to evaluate different pedagogical approaches:
- Socratic teaching (dialectical questioning)
- Constructivist teaching (concept building)
- Experiential teaching (practical application)

# Installation and housekeeping


## Create new virtual environment
```python -m venv pss-env
source pss-env/bin/activate  # On Windows: pss-env\Scripts\activate
```


## Clone repository
```
git clone https://github.com/yourusername/pss.git
cd pss
```

## Install dependencies
```
pip install -r requirements.txt
```

## Install the package in development mode
```
pip install -e .
```


# Analyses

## Data Preparation
```
# Prepare EEDI dataset
python -m prototype.data.eedi_analyzer \
    --input_file path/to/all_train.csv \
    --output_dir analysis

# Generate mock data for testing (optional)
python -m prototype.data.generate_mock_data \
    --size 1000 \
    --output mock_eedi_sample.csv
```


## Basic Validation
```
# Run basic cross-validation
python -m prototype.validation.run_validation \
    all_train.csv \
    --output_dir validation_results \
    --n_folds 5

# Run with increased sample size
python -m prototype.validation.run_validation \
    all_train.csv \
    --output_dir validation_results \
    --n_folds 10 \
    --group_size 200
```

## Advanced Analysis Options
```
# Run with specific seed for reproducibility
python -m prototype.validation.run_validation \
    all_train.csv \
    --seed 42 \
    --output_dir validation_results

# Run with enhanced stratification
python -m prototype.validation.run_validation \
    all_train.csv \
    --stratify_by misconception_type \
    --output_dir validation_results

# Generate detailed analysis report
python -m prototype.analysis.generate_report \
    validation_results/cross_validation_results.json \
    --output analysis_report.pdf
```


## Transcript Generation
```
# Generate teaching interaction transcripts
python -m prototype.run_transcript \
    --structure topics/ednet_structure.json \
    --approach socratic \
    --output transcripts/

# Generate transcripts for all approaches
for approach in socratic constructive experiential; do
    python -m prototype.run_transcript \
        --structure topics/ednet_structure.json \
        --approach $approach \
        --output transcripts/$approach/
done
```


# Output Dirctory Structure
results/
├── validation_results/
│   ├── cross_validation_results.json
│   ├── fold_*/
│   │   └── metrics.json
├── transcripts/
│   ├── socratic/
│   ├── constructive/
│   ├── experiential/
└── analysis/
    ├── analysis_results.json
    └── figures/


# Improving Statistical Results
To improve the current statistical results,  the following methodological enhancements are required

## Enhance Sample Size
```
# Run with larger group size and more folds
python -m prototype.validation.run_validation \
    all_train.csv \
    --n_folds 10 \
    --group_size 500 \
    --output_dir validation_results_enhanced
```



## Refined Stratification
```
# Run with enhanced stratification options
python -m prototype.validation.run_validation \
    all_train.csv \
    --stratify_by "misconception_type,difficulty_level" \
    --balanced_groups true \
    --output_dir validation_results_stratified
```

## Pattern Matching Improvements
```
# Run with enhanced pattern matching
python -m prototype.validation.run_validation \
    all_train.csv \
    --pattern_matching_threshold 0.8 \
    --misconception_min_occurrence 5 \
    --output_dir validation_results_patterns
```


# Contributing
See CONTRIBUTING.md 

# License
MIT

# Development Roadmap



Suggestions for Improving Statistical Analysis:

1. **Methodological Improvements:**
   - Increase minimum group size to 500 for better statistical power
   - Implement bootstrap resampling for effect size estimation
   - Add Bayesian analysis for small sample sizes
   - Enhance stratification based on misconception types

2. **Code Changes Needed:**
```python
# In eedi_cross_validator.py
def _create_balanced_groups(self, construct_stats: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Enhanced group creation with better stratification"""
    # Implement multiple stratification levels
    strata = self._create_multi_level_strata(construct_stats)
    
    # Increase minimum group size
    min_group_size = max(500, len(construct_stats) // 4)
    
    # Implement balanced sampling within each stratum
    control_group, exp_group = self._balanced_stratified_sampling(
        construct_stats,
        strata,
        min_group_size=min_group_size
    )
    
    return control_group, exp_group
```

## Priority 1: Enhanced Teaching Personas
- Develop intelligent teaching personas beyond simple pattern matching
- Implement `TeachingIntelligence` class for deep conceptual understanding
- Add real-time adaptation to student responses
- See initial implementation in `prototype/simulation/teaching_intelligence.py`
- Maintain pattern-matching persona as experimental control condition

### Key Components to Implement
- Conceptual state tracking
- Dynamic teaching path generation  
- Response adaptation system
- Learning progression monitoring

## Priority 2: Blackboard Architecture Enhancement
- Expand knowledge sources to include:
 - Three teaching strategies (Socratic, constructivist, experiential)
 - Pattern-matching control strategy
 - Student response analysis
- Implement proper control flow between knowledge sources
- Add monitoring of strategy effectiveness

## Priority 3: Data Utilization Improvements 
- Remove current artificial group size limitations
- Scale up to use larger EEDI dataset portions
- Current limitation: Only using tiny fraction of available data
- Target: Utilize at least 100,000 interactions (up from current ~1000)

## Priority 4: Statistical Analysis Enhancement
- Implement proper stratification for larger groups
- Maintain balanced groups across:
 - Misconception types
 - Student demographics
 - Topic areas
- Enable meaningful comparison between:
 - Enhanced teaching personas
 - Pattern-matching control
 - Original EEDI performance baseline

## Priority 5: Integration Testing
- Develop comprehensive test suite for enhanced personas
- Validate blackboard control mechanisms
- Test system scalability with larger data samples

## Priority 6: Documentation
- Update system architecture documentation
- Add clear examples of persona-student interactions
- Document statistical analysis procedures
- Provide examples of enhanced teaching strategies

## Success Metrics
- Demonstrable improvement over pattern-matching baseline
- Statistically significant effects with larger sample sizes
- Clear differentiation between teaching strategies
- Robust performance across different misconception types

## Current Status
- Basic persona implementation complete
- Control condition identified
- Initial statistical framework in place
- Need to scale up data utilization
- Need to implement enhanced teaching logic

## Next Steps
1. Implement enhanced teaching personas
2. Remove data size limitations
3. Scale up statistical analysis
4. Add proper stratification
5. Enhance blackboard control


