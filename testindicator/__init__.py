import os.path as path

from paths import ROOT_PATH

with open(path.join(ROOT_PATH, 'VERSION')) as version_file:
	version = version_file.read().strip()

__version__ = version
