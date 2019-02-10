CWD = $(shell pwd)

.PHONY: clean default server

default: server

server: build run

build:
	docker build -t control-panel-api:latest .

run:
	docker run --rm \
	--name control-panel-api \
	-p 8080:8080 \
	--link rover-core:rover-core \
	control-panel-api
	