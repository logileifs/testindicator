#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard library dependencies
from subprocess import Popen
from subprocess import PIPE
import threading
import logging
import time

# gi repository dependencies
from gi.repository import GLib


log = logging.getLogger(__name__)


class TestRunner(threading.Thread):
	"""Worker thread to execute tests in background"""
	def __init__(
		self,
		group=None,
		target=None,
		callback=None,
		name=None,
		args=(),
		kwargs=None,
		verbose=None):
		super(TestRunner, self).__init__(
			group=group,
			target=target,
			name=name,
			verbose=verbose
		)

		self.p = None
		self.args = args
		self.kwargs = kwargs
		self.callback = callback


	def run(self):
		log.debug('running with %s and %s', self.args, self.kwargs)
		result = self.run_cmd(*self.args)
		GLib.idle_add(self.callback, result)


	def run_cmd(self, cmd=None, cwd=None):
		result = None
		if not cmd:
			return result
		log.debug('running command ' + cmd)
		try:
			self.p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, cwd=cwd)
			while self.p.poll() is None:
				#log.debug('still working...')
				time.sleep(0.5)
			log.debug('test run done')
			stdout, stderr = self.p.communicate()
			result = self.p.returncode
		except Exception as e:
			log.debug('exception when running command %s' % cmd)
			log.debug(e)

		log.debug('TestRunner exiting with result %s', result)
		return result


	def cancel(self):
		log.debug('thread should cancel RIGHT NOW!')
		self.p.kill()
		log.debug('subprocess killed')
