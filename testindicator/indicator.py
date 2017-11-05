#!/usr/bin/env python
# -*- coding: utf-8 -*-

# gi repository dependencies
import gi

gi.require_version('AppIndicator3', '0.1')
from gi.repository.AppIndicator3 import IndicatorCategory
from gi.repository.AppIndicator3 import IndicatorStatus
from gi.repository import AppIndicator3 as appindicator

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


# standard library dependencies
import logging

# project imports
from paths import YELLOW
from paths import GREEN
from paths import RED

import config as cfg


log = logging.getLogger(__name__)


class Indicator(object):
	"""Indicator class for testindicator"""
	def __init__(self, **kwargs):
		super(Indicator, self).__init__()
		self.indicator = appindicator.Indicator.new(
			'testindicator',
			YELLOW,
			IndicatorCategory.APPLICATION_STATUS
		)
		self.status = None
		self.on_quit = kwargs.get('quit')
		self.on_run = kwargs.get('run', None)
		self.on_stop = kwargs.get('stop', None)
		self.indicator.set_status(IndicatorStatus.ACTIVE)
		self.menu = gtk.Menu()

		self.project_name = gtk.MenuItem(cfg.project_name)
		self.project_name.set_sensitive(False)
		self.project_name.show()
		self.menu.append(self.project_name)

		separator_item = gtk.SeparatorMenuItem()
		separator_item.show()
		self.menu.append(separator_item)

		self.show_item = gtk.CheckMenuItem("Notifications")
		self.show_item.set_active(cfg.notifications)
		self.show_item.connect('toggled', self.on_notifications_toggle)
		self.show_item.show()
		self.menu.append(self.show_item)

		self.run_now_item = gtk.MenuItem('Run tests (CTRL+SUPER+T)')
		self.run_now_item.connect('activate', self.run_or_stop)
		self.run_now_item.set_sensitive(True)
		self.run_now_item.show()
		self.menu.append(self.run_now_item)

		separator_item = gtk.SeparatorMenuItem()
		separator_item.show()
		self.menu.append(separator_item)

		self.item_quit = gtk.MenuItem('Exit (CTRL+SUPER+E)')
		self.item_quit.connect('activate', self.on_quit)
		self.menu.append(self.item_quit)
		self.menu.show_all()
		self.indicator.set_menu(self.menu)


	def on_notifications_toggle(self, widget, data=None):
		cfg.notifications = not cfg.notifications


	def indicate_success(self):
		log.debug('success! :)')
		self.indicator.set_icon(GREEN)


	def indicate_unkown(self):
		log.debug('unkown :/')
		self.indicator.set_icon(YELLOW)


	def indicate_failure(self):
		log.debug('failure :(')
		self.indicator.set_icon(RED)


	def run_or_stop(self, gtk_menu_item):
		if self.status == 'waiting':
			log.debug('run now')
			self.on_run()
		elif self.status == 'running':
			log.debug('cancel test run')
			self.on_stop()


	def set_status(self, status):
		log.debug('set_status to: %s' % status)
		self.status = status
		if self.status == 'running':
			log.debug('indicator status: running')
			self.run_now_item.get_child().set_text('Stop execution')
			#self.run_now_item.set_sensitive(False)
		if self.status == 'waiting':
			self.run_now_item.get_child().set_text('Run tests (CTRL+SUPER+T)')
			#self.run_now_item.set_sensitive(True)
