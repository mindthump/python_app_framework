USER_NAME ?= mindthump

.PHONY: all build build-fruit build-greet
.PHONY: deploy deploy-pvc deploy-info deploy-service
.PHONY: deploy-fruit deploy-greet drop-greet-pod
.PHONY: fresh


all: fresh build deploy

build: build-fruit build-greet

build-fruit:
	minikube image build -t mindthump/fruit-server -f fruit_server_app/Dockerfile .

build-greet:
	minikube image build -t mindthump/greet -f greet_app/Dockerfile .

deploy: deploy-pvc deploy-info deploy-fruit deploy-services deploy-greet

deploy-pvc:
	kubectl apply -f appdata-pvc.yaml

deploy-info:
	kubectl apply -f user-info-secret.yaml

deploy-fruit:
	kubectl apply -f fruit-deployment.yaml

deploy-services:
	kubectl apply -f fruit-service.yaml

deploy-greet:
	kubectl apply -f greet-deployment.yaml

drop-greet-pod:
	kubectl apply -f greet-pod.yaml

fresh:
	minikube stop
	minikube delete
	minikube config set WantUpdateNotification false
	minikube start --driver=hyperkit --container-runtime=docker
	@eval $$(minikube -p minikube docker-env)
	minikube status
