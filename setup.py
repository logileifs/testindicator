# -*- coding: utf-8 -*-

from setuptools import setup

setup(
	name='testindicator',
	packages=['testindicator'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'watchdog',
		'zenipy',
		'pyyaml'
	],
	entry_points={
		'console_scripts': [
			'testindicator = testindicator.application:main',
		]
	},
	data_files = [
		('share/applications', ['data/testindicator.desktop']),
	],
	version='0.4',
	description="Don't worry about running tests - just write code",
	long_description="testindicator is an automatic test runner/monitor. It monitors a directory of your choice and runs your tests as soon as a file is changed",
	author='Logi Leifsson',
	author_email='logileifs@gmail.com',
	url='https://github.com/logileifs/testindicator',
)
