#!/usr/bin/env python
# -*- coding: utf-8 -*-

# gi repository dependencies
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify

# standard library dependencies
import logging
import os

# project imports
from paths import YELLOW_BIG as YELLOW
from paths import GREEN_BIG as GREEN
from paths import RED_BIG as RED

import config as cfg

log = logging.getLogger(__name__)

class Notifier(object):
	"""Notifier class for testindicator"""
	def __init__(self):
		super(Notifier, self).__init__()
		notify.init('testindicator')
		self.notification = None

	def inform_success(self, msg):
		log.debug('notify success')
		self.inform(msg, GREEN)

	def inform_failure(self, msg):
		log.debug('notify failure')
		self.inform(msg, RED)

	def inform_unkown(self, msg):
		log.debug('notify unknown')
		self.inform(msg, YELLOW)
		
	def inform(self, msg, icon=None):
		if cfg.notifications:
			title = "<b>%s</b>" % cfg.project_name
			if self.notification is None:
				self.notification = notify.Notification.new(title, msg, icon)
			else:
				self.notification.update(title, msg, icon)
			#notification.set_timeout(2)
			self.notification.show()