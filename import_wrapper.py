import os
import sys
import glob
import logging

# Add 3rdparty/*.zip to sys.path so that we can import them seamlessly

#for ziplib in glob.glob(os.path.join(root, '3rdparty', '*.zip')):
#    logging.debug("Adding 3rdparty library '%s' to sys.path" % ziplib)
#    sys.path.insert(0, ziplib)

root = os.path.abspath(os.path.dirname(__file__))
tpty = os.path.join(root, '3rdparty')
for child in os.listdir(tpty):
    child = os.path.join(tpty, child)
    if os.path.isdir(child):
        dir = os.path.abspath(os.path.join(root, '3rdparty', child))
        sys.path.insert(0, dir)

import debris.rstcode 