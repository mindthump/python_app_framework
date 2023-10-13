# A Pet Demo Project

### Note the project is in perpetual flux and *might not actually run* at any given moment.

Originally, this was just samples of stuff I have been playing with in
Python. This is now primarily a **testing and experimenting application
for Kubernetes cluster administration**, particularly as preparation to
sit for the Cerified Kubernetes Administrator (CKA) exam.

The original project was all about a little framework for building
command-line utility tools. I got tired of constantly re-inventing my
own boilerplate code, and I didn't like any of the frameworks out there.
I was inspired by some libraries like `click`, but they were too much.
So this is just enough framework for my needs.

While the demo was originally just some basic python modules, when
I started consulting at Taos Mountain they encouraged me to learn
Google Cloud and Docker. To help me learn that, I converted this little
framework's sample app into docker containers, then a docker-compose
stack.

I now have this running in **Kubernetes**. It should run in pretty
much any K8s cluster. Some of my favorites for local development on my
Macbook Pro:

- Kubernetes on Vagrant boxes
- minikube
- Rancher Desktop

My current personal preference is using an
[elegant vagrant setup from TechieCamp](https://github.com/techiescamp/vagrant-kubeadm-kubernetes.git).


The application includes
[a tiny REST server](https://github.com/mindthump/python_app_framework/blob/main/fruit_server_app/fruit_server.py)
that returns a simple JSON list of fruits, so I can play with the
`requests` library. (I'm planning to do more with this later, like
migrate from Falcon to FastAPI.) Some fake user info comes in as a
secret. (The secrets stuff needs more work to be interesting, it just
let me get rid of some redundant example functionality.)

The REST server is used by a sample app, [greet.py](https://github.com/mindthump/python_app_framework/blob/main/greet_app/greet.py).

I also have an adaptation of my
[toolkit](https://github.com/mindthump/toolkit)
utility container. When it starts as part of the cluster, the entrypoint
is set to sleep for one day. This lets you open a shell on the machine
(via `kubectl exec`) and look around, run the python app, debug, or
whatever. It could also be started as an ephemeral/debugging container
in the `fruit` server pod.

### Instructions

1. Start up a kubernetes environment.

    1. Vagrant kubeadm Kubernetes, from TechieCamp

        1. Install [Vagrant by HashiCorp](https://www.vagrantup.com/)
        1. `git clone https://github.com/techiescamp/vagrant-kubeadm-kubernetes.git`
        2. `cd vagrant-kubeadm-kubernetes`
        3. `vagrant up`

    1. [minikube](https://minikube.sigs.k8s.io/docs/)

    1. [Rancher Desktop](https://rancherdesktop.io/)

2. (OPTIONAL) Build the images and push to your own registry. You can pull from
   mine, but you can't push to it; this is left as an exercise for the reader. If
   you do this, of course you'll need to adjust the other files.

3. Deploy the resources using `make`. Look in the `Makefile` for step-by-step isntructions. This will deploy:

    1. Local-path Persistent Volume and a Persistent Volume Claim for the apps to use the storage
    2. The `fruit` server Deployment and Services
    3. The `greet` application Deployment, ConfigMaps, and Secrets

4. Start the client cron job. (There is also a single-pod version, 'greet-pod.yaml' that will start and sleep for 1 day.)

    1. `kubectl apply -f greet-cronjob.yaml`

VKK has a dashboard; see their README.md file for instructions, you'll
need to use `kubectl proxy`. I like to use the Rancher Desktop Dashboard
if you're using Rancher Desktop. You could also use `k9s`, `minikube
dashboard`, or a lot of other tools.

## AppFramework

A flexible framework for python script command-line applications. Easy to
subclass, test, etc. - for my personal use but use it if you want.

Once upon a time, an organizational policy made getting libraries installed on
all the Jenkins clients difficult, the installed packages were a mess, and I
couldn't use virtual environments. I came up with a crazy hack of the python
sys.path to allow me to use local library-ish modules rather than rely on
them being installed in _site-packages_ or running `pip install -e ...`. This
made the application somewhat self-contained: it could be downloaded from a
repository and run with a stock python installation. It sucked hard, but it
solved an immediate problem.

Now, the Dockerfile copies the "app_utils" package directory, which contains
the framework and some utility code, including my custom initialize_logging()
function. It sets up a slightly more complex logging than the basic, but nothing
too complex. It can act as a pseudo-singleton, and can be extended pretty
easily. The location of log files is configurable.

(N.B. Today I would just use somethng like [icecream](https://github.com/gruns/icecream) and/or [loguru](https://github.com/Delgan/loguru) instead.)

## InstantApp

This is a super scaled-down version of the AppFramework, just enough framework
to have a nice command-line application.

### IN THE WORKS

- Type hints
- Playing with DBs
- More Secrets stuff and Ingress
- Deployment using _ArgoCD_ by a _Jenkins_ job
