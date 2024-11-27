FILE			= ./src/docker-compose.yml
DOCKER_CMD		= docker compose -f ${FILE}

BACKEND_CONTNR	= fastapi
FRONTEND_CONTNR	= react
DATABASE_CONTNR	= redis

BACKEN_IMAGE	= fastapi:custom
FRONTEND_IMAGE	= react:custom
DATABASE_IMAGE	= redis:latest

BEDB_NETWORK	= bedb
FEBE_NETWORK	= febe

all: build up

build:
	${DOCKER_CMD} build

up:
	${DOCKER_CMD} up

down:
	${DOCKER_CMD} down

goin_backend:
	docker exec -it ${BACKEND_CONTNR} /bin/bash

goin_frontend:
	docker exec -it ${FRONTEND_CONTNR} /bin/bash

goin_database:
	docker exec -it ${DATABASE_CONTNR} /bin/bash

clean: rm_containers rm_images rm_networks

prune:
	docker system prune

clean_all: clean prune

rm_containers:
	docker rm -f ${BACKEND_CONTNR} ${FRONTEND_CONTNR} ${DATABASE_CONTNR}

rm_images:
	docker rmi -f ${BACKEN_IMAGE} ${FRONTEND_IMAGE} ${DATABASE_IMAGE}

rm_networks:
	if docker network inspect ${BEDB_NETWORK} > /dev/null; then \
		docker network rm ${BEDB_NETWORK}; \
	fi

	if docker network inspect ${FEBE_NETWORK} > /dev/null; then \
		docker network rm ${FEBE_NETWORK}; \
	fi

re: clean all