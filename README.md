# A Pet Demo Project

### Note the project is in perpetual flux and *might not actually run* at any given moment.

Originally, this was just samples of stuff I'm playing with in Python. The project was all
about a little framework for building command-line utility tools. I got tired of my own boilerplate
code, and I didn't like any of the frameworks out there. I was inspired by some libraries like
`click`, but they were too much. So this is just enough framework for my needs.

While the demo was originally just some basic python modules, when I started consulting at Taos
Mountain they encouraged me to learn Google Cloud and Docker. To help me learn that, I converted
this little framework's sample app into docker containers, then a docker-compose application stack.
I now have this running in **Kubernetes**, in particular on Rancher Desktop (or `minikube`) on my
Macbook Pro.

The stack includes a tiny REST app that returns a simple JSON list of fruits, so I can play with
the `requests` library. (I'm planning to do more with this later.) I can spin up a DB container but
don't use it yet. Some fake user info comes in as a "service secret". (The secrets stuff needs more
work to be interesting, it just let me get rid of some redundant example functionality.)

All of these services are used by the framework sample app,
[greet.py](https://github.com/mindthump/python_app_framework/blob/main/greet_app/greet.py). This is
basically a sidecar-style adaptation of my [toolkit](https://github.com/mindthump/toolkit) utility
container. When it starts as part of the stack, the entrypoint is set to sleep for one day. (After
that the container will exit and stop.) This lets you open a shell on the machine and look around,
run the python app, debug, or whatever. It can also be started as an ephemeral/debugging container
in the `fruit` server pod. When it's time to promote, set the entrypoint and command as needed.

### Instructions

_The `minikube` part can be replaced with starting up Rancher Desktop, colima, or another K8s._

1. Start up a kubernetes environment
    1. Install `minikube` or another Kubernetes implementation. I'm not going to help you with that here, use the Google.
    2. `minikube start --driver=hyperkit --container-runtime=docker`
    3. `eval $(minikube docker-env)`
2. Build the images (or use docker, buildah, nerdctl, etc.)
    1. `minikube image build -t mindthump/fruit-server -f fruit_server_app/Dockerfile .`
    2. `minikube image build -t mindthump/greet -f greet_app/Dockerfile .`
3. Deploy the resources
    1. `kubectl apply appdata-pvc.yaml`
    2. `kubectl apply user-info-secret.yaml`
    3. `kubectl apply fruit-deployment.yaml`
    4. `kubectl apply greet-deployment.yaml`

Or use the Makefile.

To manage the pods, I like to use the Rancher Desktop Dashboard. You could also use `k9s`, `minikube
dashboard`, or a lot of other tools.

## AppFramework

A flexible framework for python script command-line applications. Easy to subclass, test, etc. - for
my personal use but use it if you want.

Once upon a time, an organizational policy made getting libraries installed on all the Jenkins
clients difficult, the installed packages were a mess, and I couldn't use virtual environments. I
came up with a crazy hack of the python sys.path to allow me to use local library-ish modules rather
than rely on them being installed in _site-packages_ or running `pip install -e ...`. This made the
application somewhat self-contained: it could be downloaded from a repository and run with a stock
python installation. It sucked hard, but it solved an immediate problem.

Now, the Dockerfile copies the "app_utils" package directory, which contains the framework and
some utility code, including my custom initialize_logging() function. It sets up a slightly more
complex logging than the basic, but nothing too complex. It can act as a pseudo-singleton, and can
be extended pretty easily. The location of log files is configurable.

## InstantApp

This is a super scaled-down version of the AppFramework, just enough framework to have a nice
command-line application.

### IN THE WORKS

- Type hints
- Playing with DBs
- More Secrets, Services, PVs/PVCs, and networking stuff
- Deployment using _ArgoCD_ by a _Jenkins_ job
