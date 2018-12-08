#!/usr/bin/env python
####################################################################################################
#                                                                                                  #
#   Setup file for compiling and installing the python wrapper for dasslc                          #
#                                                                                                  #
#   Author: Ataide Neto                                                                            #
#   email: ataide@peq.coppe.ufrj.br                                                                #
#   Universidade Federal do Rio de Janeiro                                                         #
#   Version: 0.1-4                                                                                 #
#   Last modification: May 4, 2018 @ 12:10                                                         #
#                                                                                                  #
####################################################################################################

from distutils.core import setup, Extension
from numpy.distutils.misc_util import get_numpy_include_dirs
import os

if os.path.exists(os.path.join("sparse","lib","sparse.a")):
    extraObjects = [os.path.join("sparse","lib","sparse.a")]
    defineMacros = [('SPARSE', None)]
else:
    extraObjects = []
    defineMacros = []

setup(
    name = 'Dasslc2py',
    version = '0.1-4',
    license = 'Free',
    author = 'ataide@peq.coppe.ufrj.br',
    ext_modules=[
        Extension("dasslc",
            sources = ["dasslcmodule.c",os.path.join("dasslc", "dasslc.c")],
            include_dirs = get_numpy_include_dirs(),
            define_macros = defineMacros,
            extra_objects = extraObjects
        )
    ]
)
