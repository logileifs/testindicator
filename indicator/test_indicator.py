#!/usr/bin/env python
from __future__ import print_function
from gi.repository.AppIndicator3 import IndicatorCategory
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import Gtk as gtk
from subprocess import call
import filemon as fm
import signal
import paths
import yaml
import sys
import os


APPINDICATOR_ID = 'testindicator'
indicator = None
full_cmd = None
excluded_files = None
notifications = True
watch_dir = None
verbose = False
icon = None
category = IndicatorCategory.SYSTEM_SERVICES


def set_watch_directory(directory):
	global watch_dir
	watch_dir = os.path.abspath(directory)


def read_config():
	global full_cmd
	global excluded_files
	global notifications
	global watch_dir
	global verbose
	with open(watch_dir + '/test.yml') as f: data = yaml.load(f)

	full_cmd = data['test']
	excluded_files = data['exclude_files']
	notifications = data.get('notifications', True)
	verbose = data.get('verbose', False)


def eprint(*args, **kwargs):
	if verbose:
		print(*args, file=sys.stderr, **kwargs)


def monitor_dir(callback):
	fmon = fm.FileMon(watch_dir, fm.IN_CLOSE_WRITE, callback, True)
	fmon.start()


def run_cmd(cmd):
	return call(cmd.split())


def handle_change(evt):
	eprint('change detected in ' + evt.pathname)
	read_config()
	file_name = evt.pathname.split('/')[-1]
	if file_name in excluded_files:
		return
	inform('Running tests')
	indicator.set_icon(paths.YELLOW)
	eprint(evt.maskname + ' detected in ' + evt.pathname)
	eprint('running tests')
	result = None
	try:
		result = call(full_cmd.split())
	except Exception as e:
		eprint('exception when running command %s' % full_cmd)
		eprint(e)
		inform('Error when running tests')
	eprint('result: %s' % result)
	if result is None:
		indicator.set_icon(paths.YELLOW)
		inform('Error while running tests')
	elif result != 0:
		eprint('result NOT 0')
		indicator.set_icon(paths.RED)
		inform('Tests failed')
	else:
		indicator.set_icon(paths.GREEN)
		inform('Tests passed')


def set_icon(new_icon):
	global icon
	icon = new_icon
	indicator.set_icon(icon)


def inform(msg):
	if notifications:
		notify.Notification.new("<b>Test Indicator</b>", msg, None).show()


def register_indicator(app_id, icon, ctgry):
	return appindicator.Indicator.new(app_id, icon, ctgry)


def setup_indicator(icon):
	global indicator
	indicator = register_indicator(APPINDICATOR_ID, icon, category)
	indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
	indicator.set_menu(build_menu())
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
	gtk.main_quit()


def run_forever():
	gtk.main()


def run(directory):
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	set_watch_directory(directory)
	read_config()
	eprint('paths.ROOT_PATH: ' + paths.ROOT_PATH)
	eprint('watching directory: %s' % watch_dir)
	eprint('full_cmd: %s' % full_cmd)
	#eprint('yaml data: %s' % data)
	#eprint('test command: %s' % data['test'])
	monitor_dir(handle_change)
	setup_indicator(paths.GREEN)
	run_forever()

if __name__ == "__main__":
	watch_dir = os.path.abspath(sys.argv[1])
	run(watch_dir)
