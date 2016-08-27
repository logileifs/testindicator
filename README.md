# testindicator
A test runner and indicator applet for Ubuntu

# Requirements
pyinotify, filemon

# Installation
`$ pip install git+https://github.com/logileifs/testindicator.git`

# Usage
create a test.yml file in your working directory that includes a bash command to run the tests  
(see sample file https://github.com/logileifs/testindicator/blob/master/test.yml)  

Then run test_indicator with working directory as argument:  
`$ ./test_indicator /home/user/path/to/project`
