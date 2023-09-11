USER_NAME ?= mindthump
DTS := $(shell date '+%Y%m%d-%H%M')
APP_NAMESPACE := paf

.PHONY: all
.PHONY: build build-fruit build-greet
.PHONY: deploy deploy-localvolume deploy-info deploy-services deploy-apps
.PHONY: redeploy
.PHONY: destroy
.PHONY: superpod

deploy: deploy-localvolume deploy-info deploy-services deploy-apps

build: build-fruit build-greet

build-fruit:
	docker image build --no-cache -t ${USER_NAME}/fruit-server:${DTS} -f fruit_server_app/Dockerfile .

build-greet:
	docker image build --no-cache -t ${USER_NAME}/greet:${DTS} -f greet_app/Dockerfile .

deploy-localvolume:
	kubectl -n ${APP_NAMESPACE} apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml
	kubectl -n ${APP_NAMESPACE} apply -f appdata-pvc.yaml

deploy-info:
	kubectl -n ${APP_NAMESPACE} apply -f user-info-secret.yaml

deploy-services:
	kubectl -n ${APP_NAMESPACE} apply -f fruit-services.yaml

deploy-apps:
	kubectl -n ${APP_NAMESPACE} apply -f fruit-deployment.yaml
	kubectl -n ${APP_NAMESPACE} apply -f greet-deployment.yaml

destroy:
	kubectl -n ${APP_NAMESPACE} delete -f fruit-deployment.yaml
	kubectl -n ${APP_NAMESPACE} delete -f greet-deployment.yaml
	kubectl -n ${APP_NAMESPACE} delete -f user-info-secret.yaml
	kubectl -n ${APP_NAMESPACE} delete -f fruit-services.yaml
	kubectl -n ${APP_NAMESPACE} delete -f appdata-pvc.yaml
	kubectl -n ${APP_NAMESPACE} delete -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml

redeploy-apps: deploy-apps
	kubectl -n ${APP_NAMESPACE} rollout restart deployment fruit-deployment
	kubectl -n ${APP_NAMESPACE} rollout restart deployment greet-deployment

superpod:
	kubectl -n ${APP_NAMESPACE} apply -f superpod.yaml

all: build deploy
