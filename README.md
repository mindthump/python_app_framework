# My Curriculum Vitae

Really, this is just samples of stuff I'm playing with in Python.
Originally this project was all about a little framework for building command-line utility tools.
I got tired of my own boilerplate code, and I didn't like any of the frameworks out there.
I was inspired by some libraries like click, but they were too much.
So this is just enough framework for my needs.

When I started consulting at Taos Mountain, they encouraged me to learn Google Cloud and Docker.
(I'm now a 'Certified Associate' at each!)
To help me learn that, I converted this little framework's sample app into a Docker application stack.

The stack includes a tiny nginx service that returns a simple JSON list of fruits, so I can play with the requests library.
My plan is to write a simple Falcon REST app to do this and more.
I start up a couchdb container but don't use it yet.
Some fake user info comes in as a "service secret". (The secrets stuff needs more work to be interesting, it just let me get rid of some redundant example functionality.)

All of these services are used by the newly-extended framework sample app, 'greet.py'.
When it starts as part of the stack, the entrypoint is set to sleep for one day. (After that the container will exit and stop.)
This lets you open a shell on the machine with the python app and look around, run and debug, whatever.
When it's time to promote, set the entrypoint and command as needed.

Pull the image, or build it:

`docker build -t mindthump/greet:latest .`

Prep a swarm (one node is fine, it's a demo) and deploy the application stack:

`docker stack deploy -c docker-compose.yml simple`

Get the ID or name of the container (with 'greet' in the name):

`docker container ls`

Open a shell on the sample app's container:

`docker container exec -it CONTAINER sh`

This will start a tiny utility standalone/non-swarm container with ties into the stack's network, volume, and secrets.
CI_LOG_DIR is where to put the framework's logs; on a persistent local volume (/data) they are appended from wherever the app is executed.

`docker container run -it --network simple_app-net -v simple_appdata:/data -v <FULL_PATH>/python_app_framework/secrets.txt:/run/secrets/user_info --env CI_LOG_DIR=/data alpine sh`

## python_app_framework

A flexible framework for python script command-line applications. Easy to subclass, test, etc. - for my personal use but use it if you want.

It addressses some issues specific to a recent situation, such as sys.path management because the locations of scripts and packages are not as "tidy" as they should be.

This also includes my initialize_logging() function. It sets up a slightly more complex logging than the basic, but nothing too complex. It can act as a pseudo-singleton, and can be extended pretty easily. The location of log files is configurable.

Once upon a time, an organizational policy made getting libraries installed on all the Jenkins clients difficult and I couldn't use virtual environments. My **toolbox directory** concept allows me to "locally install" library modules rather than rely on them being installed in _site-packages_. This makes the application somewhat self-contained: it could be downloaded from a repository and run with a stock python installation. The framework by default puts all toolbox libraries on sys.path.

One of the nicest parts of using docker for this python app: no need to fret about packages on the sys.path, etc. 
The 'toolbox' is a feature I wrote in the pre-docker days when I had to manage a very unruly sys.path and directory structure.

IMO the best way to manage packages is through docker or venv or similar. However, in my situation I could not use any of that so I needed to "carry around" the required libraries in the project itself.

If you want to use my toolbox approach, for the sample app (greet.py) you should have requests and ConfigArgParse installed in the toolbox directory (and pathlib2 if you are forced to use python 2.7 like I was).

To install libraries locally use something like this:

> pip install --target ./toolbox requests

Use caution when doing this. Compiled libraries may break if they are used on the wrong platform; I try to stick to "pure python" libraries if possible. Or use docker.

### IN THE WORKS

I'm currently putting in my own little REST responder for custom tests and experiments. I want to put the app in a loop to exercise the responder.
