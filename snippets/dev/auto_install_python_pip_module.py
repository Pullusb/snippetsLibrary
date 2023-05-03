## Auto install python module

import sys
import importlib
import subprocess

def install_module(module_name, package_name=None):
    '''Install a python module with pip or return it if already installed'''
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f'Installing Module {module_name} ....')

        subprocess.call([sys.executable, '-m', 'ensurepip'])
        subprocess.call([sys.executable, '-m', 'pip', 'install', package_name or module_name])

        module = importlib.import_module(module_name)

    return module
