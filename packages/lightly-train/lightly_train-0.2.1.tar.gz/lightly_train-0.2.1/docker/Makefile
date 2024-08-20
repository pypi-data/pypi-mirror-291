TAG ?= $(shell git rev-parse HEAD)
NAMESPACE ?= lightly
IMAGE ?= train
DOCKER_BUILDKIT=1
CONTAINER_REGISTRY=eu.gcr.io/boris-250909

VERSION = $(shell grep '__version__' ../src/lightly_train/__init__.py | sed -E 's/[^0-9.]//g')

# print all versions
.PHONY: print-versions
print-versions:
	@echo "Version: $(VERSION)"



# Build the docker image using an amd64 and CUDA base image
.PHONY: build-docker-cuda  # Export image as local docker image
build-docker-amd64-cuda: OUTPUT="type=docker"
build-docker-amd64-cuda:
	DOCKER_BUILDKIT=${DOCKER_BUILDKIT} docker buildx build \
		--file Dockerfile-amd64-cuda \
		--tag $(NAMESPACE)/$(IMAGE):$(TAG) \
		--tag $(NAMESPACE)/$(IMAGE):latest \
		--target=runtime \
		--output=$(OUTPUT) \
		..

.PHONY: develop-deploy-amd64-cuda
develop-deploy-amd64-cuda: OUTPUT="type=registry"  # Push to registry
develop-deploy-amd64-cuda: NAMESPACE="lightly-develop"
develop-deploy-amd64-cuda:
	DOCKER_BUILDKIT=${DOCKER_BUILDKIT} docker buildx build \
		--file Dockerfile-amd64-cuda \
		--tag $(CONTAINER_REGISTRY)/$(NAMESPACE)/$(IMAGE):latest \
		--tag $(CONTAINER_REGISTRY)/$(NAMESPACE)/$(IMAGE):$(TAG) \
		--target=runtime \
		--output=$(OUTPUT) \
		..

.PHONY: main-deploy-amd64-cuda
main-deploy-amd64-cuda: OUTPUT="type=registry"  # Push to registry
main-deploy-amd64-cuda: NAMESPACE="lightly-main"
main-deploy-amd64-cuda:
	DOCKER_BUILDKIT=${DOCKER_BUILDKIT} docker buildx build \
		--file Dockerfile-amd64-cuda \
		--tag $(CONTAINER_REGISTRY)/$(NAMESPACE)/$(IMAGE):latest \
		--tag $(CONTAINER_REGISTRY)/$(NAMESPACE)/$(IMAGE):$(VERSION) \
		--tag $(CONTAINER_REGISTRY)/$(NAMESPACE)/$(IMAGE):$(TAG) \
		--target=runtime \
		--output=$(OUTPUT) \
		..


DATE=$(shell date +'%Y-%m-%d-%H-%M-%S')
LIGHTLY_TRAIN_OUT ?= $(PWD)/../out/docker/$(DATE)
LIGHTLY_TRAIN_DATA ?= $(PWD)/../lightly_train_docker_test_data

.PHONY: test
test:
	@echo "Generate images"
	mkdir -p $(LIGHTLY_TRAIN_DATA)
	python -c 'from PIL import Image; [Image.new("RGB", (250, 300)).save(f"$(LIGHTLY_TRAIN_DATA)/{i}.png") for i in range(5)]'
	@echo "Test train"
	docker run --rm --shm-size=1g --user $(id -u):$(id -g) -v $(LIGHTLY_TRAIN_OUT):/out -v $(LIGHTLY_TRAIN_DATA):/data lightly/$(IMAGE):$(TAG) train model="torchvision/convnext_small" epochs=2 batch_size=2
	test -f $(LIGHTLY_TRAIN_OUT)/checkpoints/last.ckpt
	@echo "Test embed"
	docker run --rm --shm-size=1g --user $(id -u):$(id -g) -v $(LIGHTLY_TRAIN_OUT):/out -v $(LIGHTLY_TRAIN_DATA):/data lightly/train:$(TAG) embed out="/out/embeddings.csv" checkpoint="/out/checkpoints/last.ckpt" batch_size=2 format="csv"
	test `wc -l < $(LIGHTLY_TRAIN_OUT)/embeddings.csv` -eq 6
	@echo "Test export"
	docker run --rm --shm-size=1g --user $(id -u):$(id -g) -v $(LIGHTLY_TRAIN_OUT):/out -v $(LIGHTLY_TRAIN_DATA):/data lightly/train:$(TAG) export out="/out/model.pth" checkpoint="/out/checkpoints/last.ckpt" part="model" format="torch_state_dict"
	test -f $(LIGHTLY_TRAIN_OUT)/model.pth
