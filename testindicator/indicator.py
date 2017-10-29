#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('AppIndicator3', '0.1')
from gi.repository.AppIndicator3 import IndicatorCategory
from gi.repository.AppIndicator3 import IndicatorStatus
from gi.repository import AppIndicator3 as appindicator
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

import logging
log = logging.getLogger(__name__)

from paths import YELLOW
from paths import GREEN
from paths import RED

class Indicator(object):
	"""Indicator class for testindicator"""
	def __init__(self, quit):
		super(Indicator, self).__init__()
		self.indicator = appindicator.Indicator.new(
			'testindicator',
			YELLOW,
			IndicatorCategory.APPLICATION_STATUS
		)
		self.on_quit = quit
		self.indicator.set_status(IndicatorStatus.ACTIVE)
		self.menu = gtk.Menu()
		self.item_quit = gtk.MenuItem('Quit')
		self.item_quit.connect('activate', self.on_quit)
		self.menu.append(self.item_quit)
		self.menu.show_all()
		self.indicator.set_menu(self.menu)


	def indicate_success(self):
		log.debug('success! :)')
		self.indicator.set_icon(GREEN)


	def indicate_unkown(self):
		log.debug('unkown :/')
		self.indicator.set_icon(YELLOW)


	def indicate_failure(self):
		log.debug('failure :(')
		self.indicator.set_icon(RED)
