#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# gi repository dependencies
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GObject
from gi.repository import Keybinder
# from gi.repository import GLib

# zenipy is a wrapper for handy gtk dialogs
import zenipy

# standard library dependencies
import logging
import signal
import sys
import os

# project imports
from testrunner import TestRunner
from indicator import Indicator
from fsmonitor import FSMonitor
from notifier import Notifier
import config as cfg


logging.basicConfig(
	level=logging.DEBUG,
	format='[%(asctime)s] %(name)s-[%(threadName)s] %(levelname)s: %(message)s',
)
log = logging.getLogger(__name__)


class Application(object):
	"""The main gtk application for testindicator"""
	def __init__(self):
		super(Application, self).__init__()
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		self.fsmonitor = FSMonitor(self.handle_change)
		self.notifier = Notifier()
		self.indicator = Indicator(
			quit=self.gtk_quit,
			run=self.run_tests_in_background,
			stop=self.cancel_test_run)
		self.bg_thread = None
		self.status = 'waiting'
		self.setup_hotkeys()


	def setup_hotkeys(self):
		log.debug('setting up hotkeys')
		Keybinder.init()
		Keybinder.bind('<Super><Ctrl>T', self.keypress, 'run-request')
		Keybinder.bind('<Super><Ctrl>E', self.keypress, 'quit-request')


	def keypress(self, key, action):
		log.debug('KEY %s, ACTION %s' % (key, action))
		if action == 'run-request' and self.status != 'running':
			log.debug('run tests now')
			self.run_tests_in_background()
		if action == 'quit-request':
			log.debug('quit-request')
			self.quit()


	def set_status(self, status):
		self.status = status
		self.indicator.set_status(status)


	def handle_change(self, evt=None):
		log.debug('running tests')
		self.run_tests_in_background()


	def run_tests_in_background(self):
		log.debug('running tests')
		self.notifier.inform_unkown('Running tests')
		self.indicator.indicate_unkown()
		self.set_status('running')
		self.bg_thread = TestRunner(
			callback=self.handle_result,
			args=(cfg.full_cmd, cfg.work_dir)
		)
		self.bg_thread.start()


	def cancel_test_run(self):
		log.debug('cancel current test run')
		self.bg_thread.cancel()


	def handle_result(self, result):
		log.debug('handle_result %s' % result)
		self.set_status('waiting')
		if result is None:
			log.debug('indicate unkown status')
			self.indicator.indicate_unkown()
			self.notifier.inform_unkown('Error while running tests')
		elif result == -9:
			log.debug('testrun was canceled')
			self.indicator.indicate_unkown()
			self.notifier.inform_unkown('Test run canceled')
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
		GObject.threads_init()
		self.fsmonitor.start()
		self.run_tests_in_background()
		gtk.main()


	def quit(self):
		self.fsmonitor.stop()
		gtk.main_quit()


def main():
	if len(sys.argv) < 2:
		watch_dir = zenipy.file_selection(
			multiple=False,
			directory=True,
			save=False,
			confirm_overwrite=False,
			filename=None,
			title='Choose a directory to watch',
			width=20,
			height=20,
			timeout=None
		)
	else:
		watch_dir = os.path.abspath(sys.argv[1])
	if not watch_dir:
		raise SystemExit('No watch directory selected - exiting')
	cfg.set_watch_dir(watch_dir)
	cfg.read()
	app = Application()
	app.run()


if __name__ == "__main__":
	main()
