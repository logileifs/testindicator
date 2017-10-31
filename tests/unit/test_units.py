#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os
import os.path as path

from nose.tools import nottest as skip

from testindicator import paths
from testindicator.application import Application
from testindicator import config as cfg
from testindicator import fsmonitor as fsmon


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
		assert ignore == True

		no_extension = path.join(project_path, 'ignore_this_dir', 'some_file')
		ignore = fsmon.should_ignore(no_extension)
		assert ignore == True

		ignore_file = path.join(project_path, 'ignore.me')
		ignore = fsmon.should_ignore(ignore_file)
		assert ignore == True

		not_ignore = path.join(project_path, 'dont_ignore.me')
		ignore = fsmon.should_ignore(not_ignore)
		assert ignore == False


	def test_run_command(self):
		app = Application()
		assert app.run_cmd('ls') == 0
		assert app.run_cmd('grep') == 2


	def test_run_with_no_command(self):
		app = Application()
		assert app.run_cmd() is None


	#@skip
	def test_long_running_command(self):
		app = Application()
		assert app.run_cmd('sleep 5') == 0
