from sys import platform

if platform == 'linux' or platform == 'linux2':
	from indicator_ubuntu import Indicator
elif platform == 'darwin':
	print('importing mac Indicator')
	from indicator_mac import Indicator
