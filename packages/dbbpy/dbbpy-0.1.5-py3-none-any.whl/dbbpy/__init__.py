import importlib
import os
import sys

# Save the original sys.path
original_sys_path = sys.path.copy()

# Restrict sys.path to only the current directory
sys.path = [os.path.dirname(__file__)]

print("\n\n")
print(os.path.dirname(__file__))

try:
    # Attempt to load the real shared object from the current directory
    # bindings = importlib.import_module("bindings")
    from .bindings import *
    # If found, print the module's file location
    print(f"Module 'bindings' found at: {bindings.__file__}")
except ImportError:
    # Handle the case where the bindings module is not found
    print(
        "The 'bindings' shared object could not be loaded. "
        "Please compile the C++ bindings by running 'poetry run compile_bindings'."
    )

finally:
    # Restore the original sys.path
    sys.path = original_sys_path

# print("\n\nfine della mia auth\n\n")



# from .bindings import *

# from bindings import *
# import numpy as np

# n = 4
# alpha = 1.3
# lambda_ = 1.1
# omega_l = np.array([0, 3])
# sp = np.array([1200, 1250, 1300, 1350])
# strike = np.array([1290, 1295, 1295, 1300])
# bid = np.array([27.7, 27.4, 29.4, 25.0])
# ask = np.array([29.3, 29.7, 31.4, 26.9])
# pFlag = np.array([1,0,1,0])

# result = performOptimization(n, alpha, lambda_, omega_l, sp, strike, bid, ask, pFlag)
# p = result[0]
# q = result[1]

# print(p)
# print(q)
