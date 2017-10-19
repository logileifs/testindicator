#!/usr/bin/python
from __future__ import print_function
import gi
gi.require_version('AppIndicator3', '0.1')
from gi.repository.AppIndicator3 import IndicatorCategory
from gi.repository import AppIndicator3 as appindicator
gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify
from gi.repository import Gtk as gtk
from os.path import relpath
#from subprocess import call
from subprocess import Popen
from paths import YELLOW
from paths import GREEN
from paths import RED

#import filemon as fm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import threading
import signal
#import paths
import yaml
import sys
import os


APPINDICATOR_ID = 'testindicator'
indicator = None
full_cmd = None
exclude_files = None
exclude_dirs = None
notifications = True
notification = None
watch_dir = None
verbose = False
icon = None
cwd = None
category = IndicatorCategory.SYSTEM_SERVICES
observer = None


class MyHandler(FileSystemEventHandler):
	def handle_change(self, evt):
		read_config()
		if ignore(evt.src_path):
			return
		run_tests_in_background()

	def on_modified(self, event):
		eprint('change detected in ' + event.src_path)
		if event.is_directory:
			# We are getting notified about a directory
			pass
		else:
			self.handle_change(event)


def set_watch_directory(directory):
	global watch_dir
	watch_dir = os.path.abspath(directory)


def read_config():
	global full_cmd
	global exclude_files
	global exclude_dirs
	global notifications
	global watch_dir
	global verbose
	global cwd

	accepted_names = ['/test.yml', '/.test.yml', '/test.yaml', '/.test.yaml']
	for name in accepted_names:
		try:
			f = open(watch_dir + name)
			data = yaml.load(f)
			f.close()
		except: pass
		else: break

	full_cmd = data['test']
	cwd = data.get('cwd', watch_dir)
	exclude_files = data.get('exclude_files', [])
	exclude_dirs = data.get('exclude_dirs', [])
	notifications = data.get('notifications', True)
	verbose = data.get('verbose', False)


def eprint(*args, **kwargs):
	if verbose:
		print(*args, file=sys.stderr, **kwargs)


def monitor_dir(callback):
	global observer
	observer = Observer()
	observer.schedule(MyHandler(), path=watch_dir, recursive=True)
	observer.start()


def run_cmd(cmd):
	result = None
	eprint('running command ' + cmd)
	try:
		result = Popen(cmd.split(), cwd=cwd).wait()
	except Exception as e:
		eprint('exception when running command %s' % full_cmd)
		eprint(e)
		inform('Error when running tests')
	return result


def handle_result(result):
	if result is None:
		set_icon(YELLOW)
		inform('Error while running tests')
	elif result != 0:
		set_icon(RED)
		inform('Tests failed')
	else:
		set_icon(GREEN)
		inform('Tests passed')


def run_tests_in_background():
	bg_thread = threading.Thread(target=run_tests)
	bg_thread.start()


def run_tests():
	inform('Running tests')
	set_icon(YELLOW)
	eprint('running tests')
	result = run_cmd(full_cmd)
	eprint('result: %s' % result)
	handle_result(result)


def ignore(path):
	items = relpath(path, watch_dir).split('/')
	subdirs = items[0:-1]
	file_name = items[-1]
	for subdir in subdirs:
		if subdir in exclude_dirs:
			return True
	for file in exclude_files:
		if file_name == file:
			eprint('exclude file %s' % file_name)
			return True
		start = file.split('.')[0]
		if start == '*':
			end = file.split('.')[1]
			if end == file_name.split('.')[1]:
				eprint('exclude all %s files' % end)
				return True


def handle_change(evt):
	eprint('change detected in ' + evt.pathname)
	read_config()
	if ignore(evt.pathname):
		return
	run_tests_in_background()


def set_icon(new_icon):
	global icon
	icon = new_icon
	indicator.set_icon(icon)


def inform(msg):
	global notification
	if notifications:
		if notification is None:
			notification = notify.Notification.new("<b>Test Indicator</b>", msg, None)
		else:
			notification.update("<b>Test Indicator</b>", msg, None)
		#notification.set_timeout(2)
		notification.show()


def register_indicator(app_id, icon, ctgry):
	return appindicator.Indicator.new(app_id, icon, ctgry)


def setup_indicator(icon):
	global indicator
	indicator = register_indicator(APPINDICATOR_ID, icon, category)
	indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
	menu = build_menu()
	indicator.set_menu(menu)
	set_icon(icon)
	notify.init(APPINDICATOR_ID)


def build_menu():
	menu = gtk.Menu()
	item_quit = gtk.MenuItem('Quit')
	item_quit.connect('activate', quit)
	menu.append(item_quit)
	menu.show_all()
	return menu


def quit(source):
	observer.stop()
	observer.join()
	gtk.main_quit()


def run_forever():
	gtk.main()


def run(directory):
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	set_watch_directory(directory)
	read_config()
	monitor_dir(handle_change)
	setup_indicator(YELLOW)
	run_tests_in_background()
	run_forever()


if __name__ == "__main__":
	watch_dir = os.path.abspath(sys.argv[1])
	run(watch_dir)
