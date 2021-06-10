
prepare-docker-build:
	mkdir -p docker/tmp
	cp -p src/* docker/tmp

build: prepare-docker-build
	docker-compose -f docker/trainer.yml build
	rm -f -r docker/tmp

compose:
	docker-compose -f docker/trainer.yml -f docker/trainer-dev.yml up