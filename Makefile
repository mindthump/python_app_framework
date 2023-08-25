USER_NAME ?= mindthump

.PHONY: all
.PHONY: build build-fruit build-greet
.PHONY: deploy deploy-localvolume deploy-info deploy-services deploy-fruit deploy-greet

all: build deploy

build: build-fruit build-greet

deploy: deploy-localvolume deploy-info deploy-services deploy-fruit deploy-greet

build-fruit:
	docker image build --no-cache -t $(USER_NAME)/fruit-server -f fruit_server_app/Dockerfile .

build-greet:
	docker image build --no-cache -t $(USER_NAME)/greet -f greet_app/Dockerfile .

deploy-localvolume:
	kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml
	kubectl apply -f appdata-pvc.yaml

deploy-info:
	kubectl apply -f user-info-secret.yaml

deploy-services:
	kubectl apply -f fruit-service.yaml

deploy-fruit:
	kubectl apply -f fruit-deployment.yaml

deploy-greet:
	kubectl apply -f greet-deployment.yaml
