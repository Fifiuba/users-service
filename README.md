# Servicio de Usuarios
---

[![GitHub Workflow Status](https://github.com/Fifiuba/users-service/actions/workflows/test_action.yml/badge.svg?event=push)](https://github.com/Fifiuba/users-service/commits/main)
[![codecov](https://codecov.io/gh/Fifiuba/users-service/branch/main/graph/badge.svg?token=WQLIP37828)](https://codecov.io/gh/Fifiuba/users-service)
[![GitHub issues](https://img.shields.io/github/issues/Fifiuba/users-service?&style=flat-square)](https://github.com/Fifiuba/users-service/issues)
[![GitHub license](https://img.shields.io/github/license/Fifiuba/users-service?&style=flat-square)](https://github.com/Fifiuba/users-service/blob/main/LICENSE)

### App

Es el servicio de usuarios donde se crea, modifica, elimina y se accede a un usuario.

### Tecnologias 

#### Language & Libraries
* Version de python Python 3.8.5

* Version de poetry Poetry (version 1.2.0)

#### Base de datos

* Postgres

#### Servicios externos

* firebase : [a link](https://console.firebase.google.com/u/0/project/user-service-9def8/overview)


### Desarrollo 

#### Ambiente de desarrollo 

* Instrucciones para instalar herramientas
    * Poetry: [a link](https://python-poetry.org/docs/)
    * docker: [a link](https://docs.docker.com/compose/install/)

* Instrucciones para configurar el ambiente de desarrollo
    * Levantar con sh.build_network.sh
    * Se debe crear un .env. Utilizar el .env.example como guia 

### Estructura del proyecto
* El projecto posee 2 parteas pricipales: test y users_service
    * test: posee los test de las apps
    * users_service: posee toda la logica del servicio de usuarios
        * controllers: posee los controladores del sistema(los endpoint)
        * database: posee un crud de los usuarios, conexion a base de datos, modelos y schemas
        * utils: posee servicios utilizados en el servicio: firebase, token_handler y authorizacion
* Arquitectura: [a link](https://lucid.app/lucidchart/2b0082b4-0986-4100-94b0-df16a620bc21/edit?invitationId=inv_221440e6-e888-4abd-a513-a07c1c196692&page=0_0#)

### Testing

* Pasos para correr los test
    ```bash
    poetry run pytest
    ```
* Pasos para correr app localmente
    ```bash
    poetry install
    poetry run uvicorn users_service.app:app --reload
    ```

* Pasos para correr el formatter
    ```bash
    poetry run black <carpeta>
    ```
* Pasos para correr el linter
    ```bash
    poetry run flake8 <carpeta>
    ```

