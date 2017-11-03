testindicator
========================

Test Indicator is a small lightweight tool that listens for changes to your code
and executes your tests as soon as a change is detected. 


Usage
-----

Create a config named ``test.yml`` in your project root directory.
Put in it ``test: [command]`` replacing [command] with the command
to run your tests.

Testindicator comes with a desktop launcher so it can be invoked
from most/any launchers (Unity dash for example). If invoked from
launcher it will ask for a directory to monitor, give it the root
directory of your project where you now have your ``test.yml`` config

testindicator can also be launched from command line by simply running
``testindicator``. It takes a directory to monitor as an argument but
if run without arguments it will ask you what directory to monitor.


Installation
**************************************

Installation via pip::

    $ sudo pip install testindicator

Now you can run ``testindicator`` from wherever::

    $ testindicator watch_dir
