do#!/bin/bash
docker-compose up

docker run -d --name mosquitto --network=host -p 1884:1884 eclipse-mosquitto



docker run -d --name linha_producao --network=host stock-linha_producao
docker run -d --name fabrica --network=host stock-fabrica
docker run -d --name fornecedor --network=host stock-fornecedor
docker run -d --name Almoxarifado --network=host stock-Almoxarifado
docker run -d --name produto --network=host stock-produto
