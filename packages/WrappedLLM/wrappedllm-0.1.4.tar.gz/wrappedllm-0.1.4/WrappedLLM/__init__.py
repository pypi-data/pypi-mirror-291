from .LLMInitialization import Initialize
from .LLMOutput import Output
from .LLMModels import get_info

__all__ = ['Initialize', 'Output', 'get_info']

# You can add a version number if desired
__version__ = '0.1.2'

# In mypackage/__init__.py

import os

def get_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        return f.read()

