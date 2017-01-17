#!/usr/bin/python
from indicator import test_indicator
import sys
import os
watch_dir = os.path.abspath(sys.argv[1])
test_indicator.run(watch_dir)
