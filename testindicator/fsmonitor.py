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

def is_excluded_subdir(subdirs):
	for subdir in subdirs:
		if subdir in cfg.exclude_dirs:
			return True
	return False


def is_excluded_file(file_name):
	for file in cfg.exclude_files:
		log.debug('checking %s' % file)
		if file_name == file:
			log.debug('exclude file %s' % file_name)
			return True
		start, ext = splitext(file)
		log.debug('start: %s' % start)
		if start == '*':
			log.debug('we have a wildcard')
			log.debug('ext: %s' % ext)
			log.debug('ext: %s' % ext)
			if ext == splitext(file_name)[-1]:
				log.debug('exclude all %s files' % ext)
				return True


def should_ignore(path):
	log.debug('should ignore %s ?' % path)
	items = relpath(path, cfg.watch_dir).split('/')
	log.debug('items: %s' % items)
	subdirs = items[0:-1]
	log.debug('subdirs: %s' % subdirs)
	if path == cfg.cfg_path:
		log.debug('CONFIG CHANGED - RELOAD')
		cfg.read()

	if is_excluded_subdir(subdirs):
		return True

	file_name = items[-1]
	log.debug('file_name: %s' % file_name)
	if is_excluded_file(file_name):
		return True

	log.debug("don't ignore")
	return False



class MyHandler(FileSystemEventHandler):

	def __init__(self, callback):
		super(MyHandler, self).__init__()
		self.callback = callback

	def on_modified(self, event):
		log.debug('change detected in ' + event.src_path)
		if event.is_directory:
			# We are getting notified about a directory
			return
		elif not should_ignore(event.src_path):
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
