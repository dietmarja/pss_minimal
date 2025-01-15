# File: setup_minimal.py

from pathlib import Path
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup minimal prototype environment."""
    # Create directory structure
    dirs = [
        'prototype/evaluation',
        'prototype/integration',
        'prototype/simulation',
        'results'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")
    
    # Install requirements
    logger.info("Installing requirements...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ])
    
    logger.info("Setup complete!")

if __name__ == "__main__":
    setup_environment()