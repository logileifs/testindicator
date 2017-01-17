#!/usr/bin/python
from os.path import abspath
from os.path import dirname
from os.path import join

###		resource file names		###
GREENLIGHT = 'greenlight.png'
YELLOWLIGHT = 'yellowlight.png'
REDLIGHT = 'redlight.png'
###		resource file names		###

ROOT_PATH = abspath(dirname(__file__))
RES_PATH = join(ROOT_PATH, 'res')
GREEN = join(RES_PATH, GREENLIGHT)
YELLOW = join(RES_PATH, YELLOWLIGHT)
RED = join(RES_PATH, REDLIGHT)
