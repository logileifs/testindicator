#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import platform

if platform == 'linux' or platform == 'linux2':
	from notifier_ubuntu import Notifier
elif platform == 'darwin':
	print('importing mac Notifier')
	from notifier_mac import Notifier
