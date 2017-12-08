#!/usr/bin/python
from os.path import abspath
from os.path import dirname
from os.path import join

###		resource file names		###
GREENLIGHT = 'greenlight.png'
GREENLIGHT_SVG = 'greenlight.svg'
GREENLIGHT_MEDIUM = 'greenlight-medium.png'
GREENLIGHT_BIG = 'greenlight-big.png'
GREENLIGHT_MAC = 'greenlight-mac.png'
YELLOWLIGHT = 'yellowlight.png'
YELLOWLIGHT_MEDIUM = 'yellowlight-medium.png'
YELLOWLIGHT_BIG = 'yellowlight-big.png'
YELLOWLIGHT_MAC = 'yellowlight-mac.png'
REDLIGHT = 'redlight.png'
REDLIGHT_MEDIUM = 'redlight-medium.png'
REDLIGHT_BIG = 'redlight-big.png'
REDLIGHT_MAC = 'redlight-mac.png'
###		resource file names		###

ROOT_PATH = abspath(dirname(__file__))
PROJECT_PATH = dirname(ROOT_PATH)
RES_PATH = join(ROOT_PATH, 'res')
GREEN = join(RES_PATH, GREENLIGHT)
GREEN_SVG = join(RES_PATH, GREENLIGHT_SVG)
GREEN_BIG = join(RES_PATH, GREENLIGHT_BIG)
GREEN_MEDIUM = join(RES_PATH, GREENLIGHT_MEDIUM)
GREEN_MAC = join(RES_PATH, GREENLIGHT_MAC)
YELLOW = join(RES_PATH, YELLOWLIGHT)
YELLOW_BIG = join(RES_PATH, YELLOWLIGHT_BIG)
YELLOW_MEDIUM = join(RES_PATH, YELLOWLIGHT_MEDIUM)
YELLOW_MAC = join(RES_PATH, YELLOWLIGHT_MAC)
RED = join(RES_PATH, REDLIGHT)
RED_BIG = join(RES_PATH, REDLIGHT_BIG)
RED_MEDIUM = join(RES_PATH, REDLIGHT_MEDIUM)
RED_MAC = join(RES_PATH, REDLIGHT_MAC)
