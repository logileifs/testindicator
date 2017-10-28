#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

from indicator import paths
from indicator import config as cfg
from indicator import application as app


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
