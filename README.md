# python_app_framework
A flexible framework for python script command-line applications. Easy to subclass, test, etc. - for my personal use but use it if you want.

It addressses some issues specific to my current situation, such as sys.path management because the locations of scripts and packages are not as "tidy" as they should be.

This also includes my initialize_logging() function. It sets up a slightly more complex logging than the basic, but nothing too complex. It can act as a pseudo-singleton, and can be extended pretty easily.
