import sys
import subprocess
# 導入所需模組和類
__version__ = "0.9.5"

# /Users/timmylai/EasyColab/__init__.py
from .Element import * 
from .Data import Colab
from .Console import Console 
from .tool import *
from .prompts import *
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def list_requirements():
    try:
        with open('./requirements.txt', 'r') as file:
            return [line.strip() for line in file if line.strip() and not line.startswith('#')]
    except IOError:
        print("無法讀取 requirements.txt 文件")
        return []

try:
    import ipywidgets as widgets
    from IPython.display import display
except ImportError:
    packs = list_requirements()
    print("正在安裝必要的依賴...")
    for i in packs:
        install(i)
    install('ipywidgets')
    import ipywidgets as widgets
    from IPython.display import display

