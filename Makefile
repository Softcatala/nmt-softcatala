build-all: docker-build-models docker-build-use-models-tools docker-build-translate-service docker-build-translate-service-test docker-build-translate-batch

docker-build-models:
	docker build -t nmt-models . -f models/docker/Dockerfile;

docker-build-use-models-tools: docker-build-models
	docker build -t use-models-tools . -f use-models-tools/docker/Dockerfile;

docker-build-translate-service: docker-build-models
	docker build -t translate-service . -f serving/translate-service/docker/Dockerfile;

docker-build-translate-service-test: docker-build-translate-service
	docker build -t translate-service-test . -f serving/translate-service/docker/Dockerfile-test;

docker-build-translate-batch: docker-build-models
	docker build -t translate-batch . -f serving/translate-batch/docker/Dockerfile;

docker-run-translate-batch:
	docker volume create traductor-files;
	docker run -v traductor-files:/srv/data -it --rm translate-batch;

docker-run-translate-service:
	docker run -it --rm -p 8700:8700 translate-service;

docker-run-translate-service-test:
	docker run -it --rm -p 8700:8700 translate-service-test;

docker-run-all-services:
	docker-compose -f local.yml up;

test:
	cd use-models-tools && python -m nose2
	cd serving/translate-batch/ && python -m nose2
	cd serving/translate-service/ && python -m nose2
