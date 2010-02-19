# -*- coding: utf-8 -*-

import sys
import os

libpath = os.path.join(os.path.dirname(__file__), '../../lib')
srcpath = os.path.join(os.path.dirname(__file__), '../../src')

if libpath not in sys.path:
    sys.path.insert(0, libpath)

if srcpath not in sys.path:
    sys.path.insert(0, srcpath)

# Issue 772 - http://code.google.com/p/googleappengine/issues/detail?id=772.
# We must keep fix_sys_path() here until it is fixed in the dev server.
ultimate_sys_path = None
def fix_sys_path():
    global ultimate_sys_path
    if ultimate_sys_path is None:
        ultimate_sys_path = list(sys.path)
    else:
        if sys.path != ultimate_sys_path:
            sys.path[:] = ultimate_sys_path
