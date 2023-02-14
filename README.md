# A Pet Demo Project

### Note the project is in perpetual flux and *might not actually run* at any given moment.

Really, this is just samples of stuff I'm playing with in Python.
Originally this project was all about a little framework for building command-line utility tools.
I got tired of my own boilerplate code, and I didn't like any of the frameworks out there.
I was inspired by some libraries like `click`, but they were too much.
So this is just enough framework for my needs.

The demo was originally just some basic python modules. When I started consulting at Taos Mountain, they encouraged me to learn Google Cloud and Docker. To help me learn that, I converted this little framework's sample app into docker containers then a docker-compose application stack. I am now in the process of getting this to run in **Kubernetes**, in particular in `minikube` on my Macbook Pro laptop.

The stack includes a tiny service that returns a simple JSON list of fruits, so I can play with the requests library.
My plan is to write a simple Falcon REST app to do this and more.
I spin up a couchdb container but don't use it yet.
Some fake user info comes in as a "service secret". (The secrets stuff needs more work to be interesting, it just let me get rid of some redundant example functionality.)

All of these services are used by the newly-extended framework sample app, 'greet.py'.
When it starts as part of the stack, the entrypoint is set to sleep for one day. (After that the container will exit and stop.)
This lets you open a shell on the machine with the python app and look around, run and debug, whatever.
When it's time to promote, set the entrypoint and command as needed.

### TBD: Instructions to run the demo, when K8s conversion is complete.

1. Install `minikube` or another Kubernetes implementation. I'm not going to help you with that here, use the Google.
1. `minikube start --driver=hyperkit --container-runtime=docker`
2. `eval $(minikube docker-env)`
3. `minikube image build -t mindthump/fruit-server -f fruit_server_app/Dockerfile .`
3. `minikube image build -t mindthump/greet -f greet_app/Dockerfile .`
4. `kubectl apply appdata-pvc.yaml`
4. `kubectl apply user-info-secret.yaml`
4. `kubectl apply fruit-deployment.yaml`
4. `kubectl apply greet-deployment.yaml`

To manage the pods, I like to use either `k9s` or `minikube dashboard`.

## AppFramework

A flexible framework for python script command-line applications. Easy to subclass, test, etc. - for my personal use but use it if you want.

Once upon a time, an organizational policy made getting libraries installed on all the Jenkins clients difficult, the installed packages were a mess, and I couldn't use virtual environments. I came up with a crazy hack of the python sys.path to allow me to use local library-ish modules rather than rely on them being installed in _site-packages_ or running `pip install -e ...`. This made the application somewhat self-contained: it could be downloaded from a repository and run with a stock python installation. It sucked hard, but it solved an immediate problem.

Now, the Dockerfile copies the "app_utils" package directory, which contains the framework and some utility code, including my custom initialize_logging() function. It sets up a slightly more complex logging than the basic, but nothing too complex. It can act as a pseudo-singleton, and can be extended pretty easily. The location of log files is configurable.

## InstantApp

This is a super scaled-down version of the AppFramework, just enough framework to have a nicw command-line application.
### IN THE WORKS

Right now I'm focused on learning Kubernetes basics, and how all the configurations interact. I used `kompose` to convert the `docker-compose.yaml` file, so there is a lot of extra glue code that I am stripping out to make it leaner.

Eventually this will be deployed using _ArgoCD_ by a _Jenkins_ job, so there may be some miscellaneous other stuff just lying around.
