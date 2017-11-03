#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard library imports
# import os
# import yaml
import logging
import os.path as path
from threading import Timer

# nose test imports
from nose.tools import nottest as skip

# gi repository
from gi.repository import GLib

# project imports
from testindicator import paths
#from testindicator.application import Application
from testindicator import config as cfg
from testindicator import fsmonitor as fsmon
from testindicator.testrunner import TestRunner


logging.basicConfig(
	level=logging.DEBUG,
	format='[%(asctime)s] %(name)s-[%(threadName)s] %(levelname)s: %(message)s',
)
log = logging.getLogger(__name__)


# Stolen from Kiwi
def refresh_gui():
	main_context = GLib.MainContext.default()
	while main_context.pending():
		main_context.iteration(False)


class TestUnits():

	def test_can_set_directory(self):
		assert cfg.watch_dir is None
		cfg.set_watch_dir('/this/is/a/test')
		assert cfg.watch_dir == '/this/is/a/test'


	def test_greenlight_icon_is_found(self):
		assert paths.RES_PATH == paths.ROOT_PATH + '/res'
		assert paths.GREEN == paths.RES_PATH + '/' + paths.GREENLIGHT
		assert paths.YELLOW == paths.RES_PATH + '/' + paths.YELLOWLIGHT
		assert paths.RED == paths.RES_PATH + '/' + paths.REDLIGHT


	def test_assert_true(self):
		assert True


	def test_ignore(self):
		project_path = paths.PROJECT_PATH
		cfg.set_watch_dir(project_path)
		cfg.read()

		pyc_file = path.join(project_path, 'some.pyc')
		ignore = fsmon.should_ignore(pyc_file)
		assert ignore is True

		no_extension = path.join(project_path, 'ignore_this_dir', 'some_file')
		ignore = fsmon.should_ignore(no_extension)
		assert ignore is True

		ignore_file = path.join(project_path, 'ignore.me')
		ignore = fsmon.should_ignore(ignore_file)
		assert ignore is True

		not_ignore = path.join(project_path, 'dont_ignore.me')
		ignore = fsmon.should_ignore(not_ignore)
		assert ignore is False


	def test_run_command(self):
		# app = Application()
		runner = TestRunner()
		assert runner.run_cmd('ls') == 0
		assert runner.run_cmd('grep') == 2


	def test_run_with_no_command(self):
		# app = Application()
		runner = TestRunner()
		assert runner.run_cmd() is None


	def test_long_running_command(self):
		# app = Application()
		runner = TestRunner()
		assert runner.run_cmd('sleep 3') == 0


	# This is an ugly hack to test thread callback
	def testrun_can_be_canceled(self):
		wait_result = {'value': None}

		def handle_result(result):
			wait_result['value'] = result

		runner = TestRunner(
			callback=handle_result,
			args=('sleep 4', None)
		)

		stopper = Timer(1, lambda: runner.cancel())
		runner.start()
		stopper.start()
		runner.join()

		refresh_gui()

		assert wait_result['value'] == -9
