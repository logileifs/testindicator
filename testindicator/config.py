#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import yaml
import os

log = logging.getLogger(__name__)

full_cmd = None
exclude_files = []
exclude_dirs = []
notifications = True
verbose = False
watch_dir = None
work_dir = None
cfg_path = None
project_name = None


def set_watch_dir(directory):
	global watch_dir
	global project_name
	watch_dir = os.path.abspath(directory)
	project_name = os.path.basename(watch_dir)


def read():
	global full_cmd
	global exclude_files
	global exclude_dirs
	global notifications
	global watch_dir
	global verbose
	global work_dir
	global cfg_path

	log.debug('reading config')
	log.debug('watch_dir: %s' % watch_dir)

	accepted_names = ['/test.yml', '/.test.yml', '/test.yaml', '/.test.yaml']
	data = None
	for name in accepted_names:
		try:
			full_name = watch_dir + name
			log.debug('trying to open %s' % full_name)
			f = open(full_name)
			data = yaml.load(f)
			f.close()
			cfg_path = os.path.abspath(full_name)
			log.debug('cfg_path: %s' % cfg_path)
		except Exception as ex:
			log.debug('failed')
			log.debug(ex)
		else: break

	if not data:
		log.critical("couldn't find settings file")
		raise SystemExit("couldn't find settings file")

	full_cmd = data['test']
	log.debug('test command: %s' % full_cmd)
	work_dir = data.get('cwd', watch_dir)
	log.debug('working directory: %s' % work_dir)
	exclude_files = data.get('exclude_files', [])
	log.debug('excluded files: %s' % exclude_files)
	exclude_dirs = data.get('exclude_dirs', [])
	log.debug('excluded directories: %s' % exclude_dirs)
	notifications = data.get('notifications', True)
	log.debug('notifications enabled: %s' % notifications)
	verbose = data.get('verbose', False)
	log.debug('verbose: %s' % verbose)