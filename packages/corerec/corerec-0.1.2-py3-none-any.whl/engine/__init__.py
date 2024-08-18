"""
Engine
======
Maintainer: Vishesh


TL;DR
------
  1. If you're using this module, then surely you're in a testing phase for corerec.
  2. This module is not meant to be used by the end user.
  3. I'll fix the __init__; it's not yet written well. -Vishesh(Admin)

Provides
  1. Graph-based recommendation systems using neural network architectures.
  2. Various neural network modules and utilities.
  3. Training and prediction functions for graph data.

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided
with the code, and a loose standing reference guide.

We recommend exploring the docstrings using
`IPython <https://ipython.org>`_, an advanced Python shell with
TAB-completion and introspection capabilities.  See below for further
instructions.

The docstring examples assume that `engine` has been imported as ``eng``::

  >>> import engine as eng

Code snippets are indicated by three greater-than signs::

  >>> x = 42
  >>> x = x + 1

Use the built-in ``help`` function to view a function's docstring::

  >>> help(eng.train_model)
  ... # doctest: +SKIP

Available subpackages
---------------------
torch_nn
    Neural network modules and utilities.
cr_boosters
    Optimizers and boosters for training.
core_rec
    Core recommendation system components.
"""

# import os
# import sys
# import warnings

# from . import version
# from .version import __version__

# Allow distributors to run custom init code before importing engine._core
# from . import _distributor_init

# try:
#     from engine.__config__ import show as show_config
# except ImportError as e:
#     msg = """Error importing engine: you should not try to import engine from
#     its source directory; please exit the engine source tree, and relaunch
#     your python interpreter from there."""
#     raise ImportError(msg) from e

# # Ensure the submodules are correctly imported
# from engine.torch_nn import torch_nn
# from engine.cr_boosters import cr_boosters
# from engine.core_rec import core_rec

# __all__ = [
#     "torch_nn",
#     "cr_boosters",
#     "core_rec",
#     "show_config",
#     "__version__"
# ]

# def __getattr__(attr):
#     if attr == "torch_nn":
#         import engine.torch_nn as torch_nn
#         return torch_nn
#     elif attr == "cr_boosters":
#         import engine.cr_boosters as cr_boosters
#         return cr_boosters
#     elif attr == "core_rec":
#         import engine.core_rec as core_rec
#         return core_rec

#     raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")

# def __dir__():
#     public_symbols = globals().keys()
#     return list(public_symbols)

# # Pytest testing
# from engine._pytesttester import PytestTester
# test = PytestTester(__name__)
# del PytestTester

# # Remove symbols imported for internal use
# del os, sys, warnings