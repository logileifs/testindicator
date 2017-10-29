# Test Indicator
A test runner and indicator applet for Ubuntu  
Runs your tests while you write code  
## Previews
![alt tag](https://raw.githubusercontent.com/logileifs/testindicator/master/showcase2.gif)  
![alt tag](https://raw.githubusercontent.com/logileifs/testindicator/master/showcase.gif)  


# Installation
## testindicator is now available as a python package
`$ sudo pip install testindicator`  


# Usage
## Configuration
Only thing you need to do is create a `test.yml` file in your project root and put in it  
`test: executable_command` (where `executable_command` is a bash executable command to run your tests)  
For more configuration options or an example see the [sample file](https://github.com/logileifs/testindicator/blob/master/test.yml)  
## Run
Then run test_indicator with project directory as argument:  
`$ testindicator /home/user/path/to/project`  
or just  
`$ testindicator`  
it will ask you for the path to the project you are working on
