# python_app_framework
A flexible framework for python script command-line applications. Easy to subclass, test, etc. - for my personal use but use it if you want.

It addressses some issues specific to my current situation, such as sys.path management because the locations of scripts and packages are not as "tidy" as they should be.

This also includes my initialize_logging() function. It sets up a slightly more complex logging than the basic, but nothing too complex. It can act as a pseudo-singleton, and can be extended pretty easily.

Once upon a time, an organizational policy made getting libraries installed on all the Jenkins clients difficult and I couldn't use virtual environments. My **toolbox directory** concept allows me to "locally install" library modules rather than rely on them being installed in _site-packages_. This makes the application somewhat self-contained: it could be downloaded from a repository and run with a stock python installation. The framework by default puts all toolbox libraries on sys.path.

For the sample app, you should have requests, ConfigArgParse, and pathlib2 (I'm forced to use python 2.7). While IMO the best way is through venv or similar, in my situation I could not use that so I needed to "carry around" the required libraries in the project itself.

To install libraries locally use something like:

> pip install --target ./toolbox *requests*

Use caution when doing this. Compiled libraries may break if they are used on the wrong platform; I try to stick to "pure python" libraries if possible.

There's a Dockerfile for the sample app, and a docker-compose.yml file for the app plus an httpbin server.

### IN THE WORKS

I'm currently putting in my own little REST responder for custom tests and experiments. I want to put the app in a loop to exercise the responder.
