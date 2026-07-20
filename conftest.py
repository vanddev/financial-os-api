"""Pytest conftest loaded early to ensure project root is on sys.path.

This allows tests to import the `app` package without installing the project
into the virtual environment.
"""
import sys
from pathlib import Path

# Insert project root at front of sys.path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
