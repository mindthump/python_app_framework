# A Pet Demo Project

### Note the project is in perpetual flux and *might not actually run* at any given moment.

Originally, this was just samples of stuff I'm playing with in Python. The project was all
about a little framework for building command-line utility tools. I got tired of my own boilerplate
code, and I didn't like any of the frameworks out there. I was inspired by some libraries like
`click`, but they were too much. So this is just enough framework for my needs.

While the demo was originally just some basic python modules, when I started consulting at Taos
Mountain they encouraged me to learn Google Cloud and Docker. To help me learn that, I converted
this little framework's sample app into docker containers, then a docker-compose application stack.

I now have this running in **Kubernetes**. It should run in pretty much any K8s. Some of my favorites
for local development on my Macbook Pro:

- Vagrant Kubernetes (https://github.com/techiescamp/vagrant-kubeadm-kubernetes)
- minikube
- Rancher Desktop

My current personal preference is using an elegant vagrant setup on VMs (e.g., VirtualBox). I call it VKK for short:
    https://github.com/techiescamp/vagrant-kubeadm-kubernetes.git

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


1. Start up a kubernetes environment. Here's `minikube`:
    1. Install `minikube`.
    2. `minikube start --driver=hyperkit --container-runtime=docker`
    3. `eval $(minikube docker-env)`

2. Build the images (or use docker, buildah, nerdctl, kaniko, etc.) Push/load image to registry as needed.
    1. `minikube image build -t mindthump/fruit-server -f fruit_server_app/Dockerfile .`
    2. `minikube image build -t mindthump/greet -f greet_app/Dockerfile .`

3. Deploy the resources. (NOTE: #1 deploys a local-path provisioner for Persistent Volumes, #2 will create a PVC with it.)
    1. `kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml`
    2. `kubectl apply -f appdata-pvc.yaml` # Persistent Volume Claim assigning storage to the application at the path
    3. `kubectl apply -f fruit-services.yaml` # Services to open ports; node-ip:30088 on the node and fruit:80 in the cluster
    4. `kubectl apply -f fruit-deployment.yaml` # Deploy the server application
    5. `kubectl apply -f user-info-secret.yaml` # Create password secret (mounted in greet, but not used yet)

4. Start the client cron job. (There is also a single-pod version, 'greet-pod.yaml' that will start and sleep for 1 day.)
    1. `kubectl apply -f greet-cronjob.yaml`

Or use the Makefile.

To manage the pods, I like to use the Rancher Desktop Dashboard. You could also use `k9s`, `minikube
dashboard`, or a lot of other tools. VKK has a dashboard; see the README.md file for instructions.

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
