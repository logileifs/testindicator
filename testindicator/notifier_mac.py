#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pync import Notifier as ntfy

# standard library dependencies
import logging

# project imports
from paths import YELLOW_BIG as YELLOW
from paths import GREEN_BIG as GREEN
from paths import RED_BIG as RED

import config as cfg

log = logging.getLogger(__name__)


class Notifier(object):
	"""Notifier class for testindicator"""
	def __init__(self):
		#notify.init('testindicator')
		#self.notification = None
		pass

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
			title = cfg.project_name
			#if self.notification is None:
			ntfy.notify(msg, title=title, appIcon=icon)
			#else:
			#    self.notification.update(title, msg, icon)
			#notification.set_timeout(2)
			#self.notification.show()
