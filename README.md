# testindicator
A test runner and indicator applet for Ubuntu  
![alt tag](https://raw.githubusercontent.com/logileifs/testindicator/master/showcase.gif)

# Requirements
[pyinotify](https://github.com/seb-m/pyinotify)  
[filemon](https://github.com/logileifs/filemon)

# Installation
`$ pip install git+https://github.com/logileifs/testindicator.git`

# Usage
create a test.yml file in your working directory that includes a bash command to run the tests  
(see sample file https://github.com/logileifs/testindicator/blob/master/test.yml)  

Then run test_indicator with working directory as argument:  
`$ ./test_indicator /home/user/path/to/project`
