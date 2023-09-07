USER_NAME ?= mindthump
DTS := $(shell date '+%Y%m%d-%H%M')

.PHONY: all
.PHONY: build build-fruit build-greet
.PHONY: deploy deploy-localvolume deploy-info deploy-services deploy-apps
.PHONY: destroy

deploy: deploy-localvolume deploy-info deploy-services deploy-apps

build: build-fruit build-greet

build-fruit:
	docker image build --no-cache -t ${USER_NAME}/fruit-server:${DTS} -f fruit_server_app/Dockerfile .

build-greet:
	docker image build --no-cache -t ${USER_NAME}/greet:${DTS} -f greet_app/Dockerfile .

deploy-localvolume:
	kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml
	kubectl apply -f appdata-pvc.yaml

deploy-info:
	kubectl apply -f user-info-secret.yaml

deploy-services:
	kubectl apply -f fruit-services.yaml

deploy-apps:
	kubectl apply -f fruit-deployment.yaml
	kubectl apply -f greet-deployment.yaml

destroy:
	kubectl delete -f fruit-deployment.yaml
	kubectl delete -f greet-deployment.yaml
	kubectl delete -f user-info-secret.yaml
	kubectl delete -f fruit-services.yaml
	kubectl delete -f appdata-pvc.yaml
	kubectl delete -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml

all: build deploy
