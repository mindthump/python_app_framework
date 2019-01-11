# python_app_framework
A flexible framework for python script command-line applications. Easy to subclass, test, etc. - for my personal use but use it if you want.

It addressses some issues specific to my current situation, such as sys.path management because the locations of scripts and packages are not as "tidy" as they should be.

This also includes my initialize_logging() function. It sets up a slightly more complex logging than the basic, but nothing too complex. It can act as a pseudo-singleton, and can be extended pretty easily.

My organization's policy makes getting libraries installed on all the clients difficult (nor can I use virtual environments), so I just carry them around myself. 
The "toolbox" directory allows me to "locally install" library modules rather than rely on them being installed in the python site-packages. I did not check in the libraries themselves.

For the sample app, you should have requests, ConfigArgParse, and pathlib2 (I'm forced to use python 2.7). To install libraries locally use something like:

pip install --target ./toolbox *requests*

Use caution when doing this. Compiled libraries may break if they are used on the wrong platform; I try to stick to "pure python" libraries if possible.