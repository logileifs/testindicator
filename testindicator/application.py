#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

# gi repository dependencies
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GLib

# zenipy is a wrapper for handy gtk dialogs
import zenipy

# standard library dependencies
from subprocess import Popen
from subprocess import PIPE
import threading
import logging
import signal
import sys
import os

# project imports
from indicator import Indicator
from notifier import Notifier
from fsmonitor import FSMonitor
import config as cfg



logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s-%(name)s[%(threadName)s] %(levelname)s: %(message)s',
)
log = logging.getLogger(__name__)


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
