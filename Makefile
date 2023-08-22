USER_NAME ?= mindthump

.PHONY: all build build-fruit build-greet
.PHONY: deploy deploy-pv deploy-pvc deploy-info deploy-service
.PHONY: deploy-fruit deploy-greet drop-greet-pod

all: build deploy

build: build-fruit build-greet

greet: build-greet deploy-greet

fruit: build-fruit deploy-pv deploy-pvc deploy-fruit

build-fruit:
	docker image build --no-cache -t $(USER_NAME)/fruit-server -f fruit_server_app/Dockerfile .

build-greet:
	docker image build --no-cache -t $(USER_NAME)/greet -f greet_app/Dockerfile .

deploy: deploy-pv deploy-pvc deploy-info deploy-fruit deploy-services deploy-greet

deploy-pv:
	kubectl apply -f appdata-pv.yaml

deploy-pvc:
	kubectl apply -f appdata-pvc.yaml

deploy-info:
	kubectl apply -f user-info-secret.yaml

deploy-services:
	kubectl apply -f fruit-service-nodeport.yaml

deploy-fruit:
	kubectl apply -f fruit-deployment.yaml

deploy-greet:
	kubectl apply -f greet-deployment.yaml

drop-greet-pod:
	kubectl apply -f greet-pod.yaml
