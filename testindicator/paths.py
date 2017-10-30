#!/usr/bin/python
from os.path import abspath
from os.path import dirname
from os.path import join

###		resource file names		###
GREENLIGHT = 'greenlight.png'
GREENLIGHT_BIG = 'greenlight-big.png'
YELLOWLIGHT = 'yellowlight.png'
YELLOWLIGHT_BIG = 'yellowlight-big.png'
REDLIGHT = 'redlight.png'
REDLIGHT_BIG = 'redlight-big.png'
###		resource file names		###

ROOT_PATH = abspath(dirname(__file__))
PROJECT_PATH = dirname(ROOT_PATH)
RES_PATH = join(ROOT_PATH, 'res')
GREEN = join(RES_PATH, GREENLIGHT)
GREEN_BIG = join(RES_PATH, GREENLIGHT_BIG)
YELLOW = join(RES_PATH, YELLOWLIGHT)
YELLOW_BIG = join(RES_PATH, YELLOWLIGHT_BIG)
RED = join(RES_PATH, REDLIGHT)
RED_BIG = join(RES_PATH, REDLIGHT_BIG)
