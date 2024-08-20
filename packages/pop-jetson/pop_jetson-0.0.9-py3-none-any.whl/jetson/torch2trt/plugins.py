import sys
import os, subprocess


version_info = sys.version_info

def __bootstrap__():
    global __bootstrap__, __loader__, __file__
    import sys, importlib.util
    
    for path in sys.path:
        if os.path.exists(os.path.join(path, 'plugins.cpython-aarch64-linux-gnu.so')):
            __file__ = os.path.join(path, 'plugins.cpython-aarch64-linux-gnu.so')
            
    __loader__ = None; del __bootstrap__, __loader__
    spec = importlib.util.spec_from_file_location(__name__,__file__)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
__bootstrap__()
