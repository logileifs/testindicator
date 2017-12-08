#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

# standard library dependencies
import logging

# project imports
from paths import YELLOW_MAC as YELLOW
from paths import GREEN_MAC as GREEN
from paths import RED_MAC as RED

log = logging.getLogger(__name__)


class Indicator(object):

	def __init__(self, **kwargs):
		self.indicator = gtk.StatusIcon()
		self.indicator.set_from_stock(gtk.STOCK_ABOUT)
		self.indicator.connect('popup-menu', self.on_right_click)
		self.indicator.set_tooltip_text('testindicator')

	def on_right_click(self, icon, event_button, event_time):
		self.make_menu(event_button, event_time)

	def make_menu(self, event_button, event_time):
		menu = gtk.Menu()

		# show about dialog
		about = gtk.MenuItem("About")
		about.show()
		menu.append(about)
		about.connect('activate', self.show_about_dialog)

		# add quit item
		quit = gtk.MenuItem("Quit")
		quit.show()
		menu.append(quit)
		quit.connect('activate', gtk.main_quit)

		menu.popup(None, None, None, None, event_button, event_time)

	def set_status(self, status):
		log.debug('set_status to: %s' % status)
		self.status = status
		if self.status == 'running':
			log.debug('indicator status: running')
			#self.run_now_item.get_child().set_text('Stop execution')
			#self.run_now_item.set_sensitive(False)
		if self.status == 'waiting':
			log.debug('indicator status: waiting')
			#self.run_now_item.get_child().set_text('Run tests (CTRL+SUPER+T)')
			#self.run_now_item.set_sensitive(True)

	def indicate_success(self):
		log.debug('success! :)')
		self.indicator.set_from_file(GREEN)

	def indicate_unkown(self):
		#log.debug('unkown :/')
		self.indicator.set_from_file(YELLOW)

	def indicate_failure(self):
		log.debug('failure :(')
		self.indicator.set_from_file(RED)

	def show_about_dialog(self, widget):
		about_dialog = gtk.AboutDialog()
		about_dialog.set_destroy_with_parent(True)
		about_dialog.set_icon_name("SystrayIcon")
		about_dialog.set_name('SystrayIcon')
		about_dialog.run()
		about_dialog.destroy()
