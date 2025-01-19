# Persona Simulation System (PSS)

An AI-first approach to teaching strategy evaluation using simulated teacher-student interactions based on the EEDI dataset.

## Overview

PSS transforms static EEDI misconception data into dynamic teaching simulations to evaluate different pedagogical approaches:
- Socratic teaching (dialectical questioning)
- Constructivist teaching (concept building)
- Experiential teaching (practical application)

## Installation


# Create new virtual environment
```python -m venv pss-env
source pss-env/bin/activate  # On Windows: pss-env\Scripts\activate
```


# Clone repository
git clone https://github.com/yourusername/pss.git
cd pss

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .



# Development Roadmap

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


