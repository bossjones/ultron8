container_name := ultron8-hacking
docker_registry_url := index.docker.io/bossjones

GIT_BRANCH  = $(shell git rev-parse --abbrev-ref HEAD)
GIT_SHA     = $(shell git rev-parse HEAD)
BUILD_DATE  = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
VERSION     ?= 0.1.0


TAG ?= $(VERSION)
ifeq ($(TAG),@branch)
	override TAG = $(shell git symbolic-ref --short HEAD)
	@echo $(value TAG)
endif

bash:
	docker run --rm -i -t --entrypoint "bash" $(docker_registry_url)/$(container_name):latest -l

build:
	docker build --tag $(docker_registry_url)/$(container_name):$(GIT_SHA) . ; \
	docker tag $(docker_registry_url)/$(container_name):$(GIT_SHA) $(docker_registry_url)/$(container_name):latest
	docker tag $(docker_registry_url)/$(container_name):$(GIT_SHA) $(docker_registry_url)/$(container_name):$(TAG)

build-force:
	docker build --rm --force-rm --pull --no-cache -t $(docker_registry_url)/$(container_name):$(GIT_SHA) . ; \
	docker tag $(docker_registry_url)/$(container_name):$(GIT_SHA) $(docker_registry_url)/$(container_name):latest
	docker tag $(docker_registry_url)/$(container_name):$(GIT_SHA) $(docker_registry_url)/$(container_name):$(TAG)

tag:
	docker tag $(docker_registry_url)/$(container_name):$(GIT_SHA) $(docker_registry_url)/$(container_name):latest
	docker tag $(docker_registry_url)/$(container_name):$(GIT_SHA) $(docker_registry_url)/$(container_name):$(TAG)

build-push: build tag
	docker push $(docker_registry_url)/$(container_name):latest
	docker push $(docker_registry_url)/$(container_name):$(GIT_SHA)
	docker push $(docker_registry_url)/$(container_name):$(TAG)

push:
	docker push $(docker_registry_url)/$(container_name):latest
	docker push $(docker_registry_url)/$(container_name):$(GIT_SHA)
	docker push $(docker_registry_url)/$(container_name):$(TAG)

push-force: build-force push

release: push
	git tag $(VERSION)
	git push upstream --tags

ci:
	docker run --rm -w /app \
	-v "$(CURRENT_DIR):/app" \
	$(docker_registry_url)/$(container_name):$(GIT_SHA) --version

dc-build:
	GID=$(shell id -g) UID=$(shell id -u) docker-compose
