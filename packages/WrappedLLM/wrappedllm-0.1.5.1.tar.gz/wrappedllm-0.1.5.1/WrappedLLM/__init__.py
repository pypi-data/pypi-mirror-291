from .LLMInitialization import Initialize
from .LLMOutput import Output
from .LLMModels import get_info
import os

__all__ = ['Initialize', 'Output', 'get_info']

# You can add a version number if desired
__version__ = '0.1.2'

# In mypackage/__init__.py


def get_readme():
    """Return the content of the README.md file."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as file:
        return file.read()

