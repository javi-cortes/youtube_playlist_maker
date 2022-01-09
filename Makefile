help:
	@echo "help                               -- prints this help"
	@echo "build                              -- builds Docker containers"
	@echo "run                                -- start the crawling"

# @ is to hide the echo of the command
# dkc = docker-compose -f docker-compose.dev.yml -f docker-compose.override.yml $arguments

GREEN="\\e[32m"
BLUE="\\e[94m"
REGULAR="\\e[39m"
RED="\\e[91m"

run:
	docker run youtube-crawler

build:
	docker build . -t youtube-crawler

.PHONY: help build run
