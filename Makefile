USER_NAME ?= mindthump
DTS := $(shell date '+%Y%m%d-%H%M')
APP_NAMESPACE := paf

.PHONY: all
.PHONY: build build-fruit build-greet
.PHONY: namespace
.PHONY: deploy deploy-localvolume deploy-info deploy-services deploy-apps
.PHONY: redeploy
.PHONY: destroy
.PHONY: toolkit

deploy: namespace deploy-localvolume deploy-info deploy-services deploy-apps

build: build-fruit build-greet

build-fruit:
	docker image build --no-cache -t ${USER_NAME}/fruit-server:${DTS} -f fruit_server_app/Dockerfile .

build-greet:
	docker image build --no-cache -t ${USER_NAME}/greet:${DTS} -f greet_app/Dockerfile .

namespace:
	-kubectl create namespace paf

deploy-localvolume:
	kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml
	kubectl -n ${APP_NAMESPACE} apply -f appdata-pvc.yaml

deploy-info:
	kubectl -n ${APP_NAMESPACE} apply -f user-info-secret.yaml
	kubectl -n ${APP_NAMESPACE} apply -f users-cm.yaml

deploy-services:
	kubectl -n ${APP_NAMESPACE} apply -f fruit-services.yaml

deploy-apps:
	kubectl -n ${APP_NAMESPACE} apply -f fruit.yaml
	kubectl -n ${APP_NAMESPACE} apply -f greet.yaml

destroy:
	kubectl -n ${APP_NAMESPACE} delete -f fruit.yaml
	kubectl -n ${APP_NAMESPACE} delete -f greet.yaml
	kubectl -n ${APP_NAMESPACE} delete -f user-info-secret.yaml
	kubectl -n ${APP_NAMESPACE} delete -f fruit-services.yaml
	kubectl -n ${APP_NAMESPACE} delete -f appdata-pvc.yaml
	kubectl -n ${APP_NAMESPACE} delete -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml
	kubectl delete ${APP_NAMESPACE}

redeploy-apps: deploy-apps
	kubectl -n ${APP_NAMESPACE} rollout restart deployment fruit
	kubectl -n ${APP_NAMESPACE} rollout restart deployment greet

toolkit:
	kubectl -n ${APP_NAMESPACE} apply -f toolkit.yaml

all: build deploy
