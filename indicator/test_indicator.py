#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

# gi repository dependencies
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GLib

# standard library dependencies
from os.path import relpath
from subprocess import Popen
from subprocess import PIPE
import threading
import logging
import signal
import yaml
import sys
import os

# project imports
from indicator import Indicator
from notifier import Notifier
from fsmonitor import FSMonitor
import config as cfg



logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s %(name)s:%(threadName)s.%(levelname)s: %(message)s',
)
log = logging.getLogger('main')


class Application(object):
	"""The main gtk application for testindicator"""
	def __init__(self):
		super(Application, self).__init__()
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		self.fsmonitor = FSMonitor(self.handle_change)
		self.notifier = Notifier()
		self.indicator = Indicator(quit=self.gtk_quit)


	def handle_change(self, evt=None):
		log.debug('running tests')
		self.run_tests_in_background()


	def run_tests_in_background(self):
		log.debug('running tests')
		self.notifier.inform_unkown('Running tests')
		self.indicator.indicate_unkown()
		bg_thread = threading.Thread(target=self.run_tests)
		bg_thread.start()


	def run_tests(self):
		result = self.run_cmd()
		log.debug('result: %s' % result)
		GLib.idle_add(self.handle_result, result)


	def run_cmd(self):
		result = None
		cmd = cfg.full_cmd
		log.debug('running command ' + cmd)
		try:
			p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, cwd=cfg.work_dir)
			stdout, stderr = p.communicate()
			result = p.returncode
		except Exception as e:
			log.debug('exception when running command %s' % cmd)
			log.debug(e)
		return result


	def handle_result(self, result):
		log.debug('handle_result %s' % result)
		if result is None:
			log.debug('indicate unkown status')
			self.indicator.indicate_unkown()
			self.notifier.inform_unkown('Error while running tests')
		elif result != 0:
			log.debug('indicate failure')
			self.indicator.indicate_failure()
			self.notifier.inform_failure('Tests failed')
		else:
			log.debug('indicate success')
			self.indicator.indicate_success()
			self.notifier.inform_success('Tests passed')


	def gtk_quit(self, source):
		log.debug('gtk_quit')
		self.quit()


	def run(self):
		self.fsmonitor.start()
		self.run_tests_in_background()
		gtk.main()


	def quit(self):
		self.fsmonitor.stop()
		gtk.main_quit()


if __name__ == "__main__":
	watch_dir = os.path.abspath(sys.argv[1])
	cfg.set_watch_dir(watch_dir)
	cfg.read()
	app = Application()
	app.run()
