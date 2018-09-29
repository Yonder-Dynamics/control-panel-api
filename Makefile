CWD = $(shell pwd)

SWAGGER_BUILD = build/swagger

SERVER_SRC = src

SWAGGER_CONTROLLERS = $(SWAGGER_BUILD)/python/swagger_server/controllers/

SWAGGER_TARGET = $(SWAGGER_BUILD)/python/swagger_server/swagger/swagger.yaml

DOCKER_CLI = docker run --rm -v $(PWD):/local swaggerapi/swagger-codegen-cli

JAVA_CLI = java -jar swagger-codegen-cli.jar

.PHONY: clean default server

default: server

$(SWAGGER_TARGET): swagger.json $(SERVER_SRC)/*
	$(JAVA_CLI) generate \
		-i swagger.json \
		-l python-flask \
		-o $(SWAGGER_BUILD)/python
	cp src/* $(SWAGGER_CONTROLLERS)	
	touch $(SWAGGER_TARGET)
	echo "\nredis" >> $(SWAGGER_BUILD)/python/requirements.txt

server: $(SWAGGER_TARGET)
	cd $(CWD)/$(SWAGGER_BUILD)/python && 		    \
	docker build -t swagger_server . && 			\
	docker run -it --rm -p 8080:8080 --link rover-core:rover-core swagger_server

clean:
	rm -rf $(SWAGGER_BUILD)
