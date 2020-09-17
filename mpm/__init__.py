"""Main Package Manager.
Author: Dodo325
GitHub: https://github.com/dodo325/mpm
"""
import sys
__version__ = "0.2.0"

def getAbout() -> str:
    info = sys.modules[__name__].__doc__
    info += "Version: " + __version__
    return info
