import sys
import subprocess
# 導入所需模組和類
__version__ = "0.9.9"

# /Users/timmylai/EasyColab/__init__.py
from .Element import *
from .Console import *
from .Client import *
from .prompts import *
from .tool import *
from .tunnel import *
import config

__all__ = ["Console", "config"]
def main():
    pass