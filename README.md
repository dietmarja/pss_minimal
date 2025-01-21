Persona Simulation System (PSS)

An AI-first approach to teaching strategy evaluation using simulated teacher-student interactions based on the EEDI dataset. The system transforms static EEDI misconception data into dynamic teaching simulations, evaluated through cross-validation.

Key Features

Dynamic teacher-student interaction simulation

Integration with EEDI misconception data

Three teaching approaches plus control condition:

Socratic teaching (dialectical questioning)

Constructivist teaching (concept building)

Experiential teaching (practical application)

Pattern-matching (control condition)

Statistical cross-validation framework

Installation and Setup

# Create virtual environment
python -m venv pss-env
source pss-env/bin/activate  # On Windows: pss-env\Scripts\activate

# Clone Repository
git clone https://github.com/yourusername/pss.git
cd pss

# Install Dependencies and Package
pip install -r requirements.txt
pip install -e .

Testing

# Run test cross-validator with minimal data
python -m prototype.tests.test_cross_validator

# Run specific teaching persona tests
python -m prototype.tests.test_teaching_personas

# Run integration tests
python -m prototype.tests.test_integration

Enhanced Teaching Simulation

The system now implements dynamic teaching interactions:

# Run enhanced teaching simulation
python -m prototype.simulation.run_enhanced_simulation \
    --data_path="prototype/data/eedi_processed.csv" \
    --knowledge_base="prototype/data/knowledge_base.json" \
    --output_dir="results/enhanced_teaching/" \
    --teaching_style="socratic" \
    --log_level=DEBUG

Cross-Validation Analysis

# Basic cross-validation
python -m prototype.validation.run_validation \
    --data_path="prototype/data/eedi_processed.csv" \
    --n_folds=5 \
    --output_dir="validation_results"

# Enhanced validation with larger samples
python -m prototype.validation.run_validation \
    --data_path="prototype/data/eedi_processed.csv" \
    --n_folds=10 \
    --group_size=500 \
    --stratify_by="misconception_type" \
    --output_dir="validation_results_enhanced"

Project Structure

prototype/
├── data/                      # Data and knowledge bases
├── simulation/               # Teaching simulation
│   ├── base_types.py        # Base classes
│   ├── teaching_personas.py # Teaching implementations
│   └── teaching_intelligence.py
├── validation/              # Cross-validation framework
│   └── eedi_cross_validator.py
├── tests/                   # Test suite
└── results/              # Analysis outputs

Current Limitations and Future Work

Statistical Analysis Improvements

Increase sample sizes (target: 500+ per group)

Implement bootstrap-based effect size estimation

Add Bayesian analysis for small samples

Enhance stratification based on misconception patterns

Teaching Simulation Enhancements

Improve teaching persona adaptation

Add real-time strategy adjustment

Implement more sophisticated dialogue generation

Enhance misconception pattern detection

Integration Improvements

Better coupling between simulation and validation

Enhanced data utilization

Improved measurement of teaching effectiveness

More sophisticated statistical analysis

Known Issues

Limited sample sizes affecting statistical power

Basic pattern matching in control condition

Stratification failures with small data sets

Simple teaching dialogue generation

Contributing

See CONTRIBUTING.md for guidelines.

License

MIT

PSS Commands Quick Reference

# CENTRAL COMMAND: Run complete PSS analysis
python -m prototype.run_pss_analysis \
    --data_path="prototype/data/eedi_processed.csv" \
    --output_dir="results/full_analysis" \
    --n_folds=10 \
    --group_size=500 \
    --all_approaches=true \
    --generate_stats=true \
    --stratify_by="misconception_type" \
    --seed=42

# This command:
# - Runs all teaching approaches (Socratic, Constructivist, Experiential, Control)
# - Uses maximum available EEDI data
# - Performs complete cross-validation
# - Generates comprehensive statistical analysis
# - Creates detailed teaching transcripts
# - Outputs combined results and comparisons

# Generate mock data for testing
python -m prototype.data.generate_mock_data --size 1000 --output mock_eedi_sample.csv
# Creates test dataset with simulated misconceptions

# Run basic test of cross-validator
python -m prototype.tests.test_cross_validator
# Tests cross-validation with minimal synthetic data

# Run enhanced teaching simulation with Socratic approach
python -m prototype.simulation.run_enhanced_simulation --teaching_style="socratic"
# Runs AI-driven teaching simulation with specified strategy

# Run basic cross-validation
python -m prototype.validation.run_validation --n_folds=5
# Performs statistical validation of teaching effectiveness

# Run with enhanced stratification
python -m prototype.validation.run_validation --stratify_by="misconception_type"
# Validates with improved group balancing

# Generate teaching interaction transcripts
python -m prototype.run_transcript --approach socratic
# Creates detailed logs of teaching interactions

# Run with specific seed for reproducibility
python -m prototype.validation.run_validation --seed 42
# Ensures reproducible results in validation

# Run with larger groups for better statistics
python -m prototype.validation.run_validation --group_size 500
# Improves statistical power through larger samples

# Generate analysis report
python -m prototype.analysis.generate_report validation_results/cross_validation_results.json
# Creates comprehensive statistical analysis report









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


