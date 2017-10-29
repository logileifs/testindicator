#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os

from testindicator import paths
from testindicator import config as cfg
from testindicator import application as app
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

	#def test_can_set_icon(self):
	#	assert ti.icon is None
	#	ti.setup_indicator(paths.GREEN)
	#	assert ti.icon is not None
	#	ti.set_icon(paths.YELLOW)
	#	assert ti.icon == paths.YELLOW

	def test_wait_a_few_seconds(self):
		import time
		time.sleep(1)
		assert True

	def test_add_new_test(self):
		assert True

	def test_ignore(self):
		#handler = MyHandler(None)
		#print('ROOT_PATH: ' + paths.ROOT_PATH)
		project_path = os.path.dirname(paths.ROOT_PATH)
		print('project_path: %s' % project_path)
		cfg.set_watch_dir(project_path)
		cfg.read()
		ignore = fsmon.should_ignore('/home/logi/repos/testindicator/some.pyc')
		assert ignore == True

		ignore = fsmon.should_ignore('/home/logi/repos/testindicator/ignore_this_dir/some_file')
		assert ignore == True

		ignore = fsmon.should_ignore('/home/logi/repos/testindicator/ignore.me')
		assert ignore == True

		ignore = fsmon.should_ignore('/home/logi/repos/testindicator/dont_ignore.me')
		assert ignore == False
