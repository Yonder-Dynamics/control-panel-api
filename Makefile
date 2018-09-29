CWD = $(shell pwd)

SWAGGER_BUILD = build/swagger

SERVER_SRC = src

SWAGGER_CONTROLLERS = $(SWAGGER_BUILD)/python/swagger_server/controllers/

SWAGGER_TARGET = $(SWAGGER_BUILD)/python/swagger_server/swagger/swagger.yaml

.PHONY: clean default server

default: server

$(SWAGGER_TARGET): swagger.json $(SERVER_SRC)/*
	docker run --rm -v $(PWD):/local swaggerapi/swagger-codegen-cli generate \
		-i /local/swagger.json \
		-l python-flask \
		-o /local/$(SWAGGER_BUILD)/python
	cp src/* $(SWAGGER_CONTROLLERS)	
	touch $(SWAGGER_TARGET)

server: $(SWAGGER_TARGET)
	cd $(CWD)/$(SWAGGER_BUILD)/python && 		    \
	docker build -t swagger_server . && 			\
	docker run -it --rm -p 8080:8080 swagger_server

clean:
	rm -rf $(SWAGGER_BUILD)