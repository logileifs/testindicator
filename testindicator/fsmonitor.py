#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from os.path import relpath
from os.path import splitext

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# project imports
import config as cfg

log = logging.getLogger(__name__)

class MyHandler(FileSystemEventHandler):

	def __init__(self, callback):
		super(MyHandler, self).__init__()
		self.callback = callback

	def should_ignore(self, path):
		log.debug('should ignore %s ?' % path)
		items = relpath(path, cfg.watch_dir).split('/')
		subdirs = items[0:-1]
		file_name = items[-1]
		if path == cfg.cfg_path:
			log.debug('CONFIG CHANGED - RELOAD')
			cfg.read()
		for subdir in subdirs:
			if subdir in cfg.exclude_dirs:
				return True
		for file in cfg.exclude_files:
			if file_name == file:
				log.debug('exclude file %s' % file_name)
				return True
			start = file.split('.')[0]
			if start == '*':
				end = file.split('.')[1]
				if end == splitext(file_name)[-1]:
					log.debug('exclude all %s files' % end)
					return True

		return False


	def on_modified(self, event):
		log.debug('change detected in ' + event.src_path)
		if event.is_directory:
			# We are getting notified about a directory
			return
		elif not self.should_ignore(event.src_path):
			self.callback(event)


class FSMonitor(object):
	"""Class to monitor file system events"""
	def __init__(self, callback):
		super(FSMonitor, self).__init__()
		self.callback = callback
		self.observer = Observer()
		handler = MyHandler(callback)
		self.observer.schedule(handler, path=cfg.watch_dir, recursive=True)

	def call_back(self):
		log.debug('calling back')
		self.callback()

	def start(self):
		self.observer.start()

	def stop(self):
		self.observer.stop()
		self.observer.join()
