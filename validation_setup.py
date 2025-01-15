# validation_setup.py
def setup_experimental_groups():
    """
    Create matched experimental and control groups from EdNet data
    - Ensure balanced demographics
    - Match prior knowledge levels
    - Account for learning history
    """
    return {
        'control': control_group,
        'experimental': experimental_group,
        'baseline': baseline_group
    }
