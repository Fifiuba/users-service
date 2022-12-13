# Servicio de Usuarios
---

[![GitHub Workflow Status](https://github.com/Fifiuba/users-service/actions/workflows/test_action.yml/badge.svg?event=push)](https://github.com/Fifiuba/users-service/commits/main)
[![codecov](https://codecov.io/gh/Fifiuba/users-service/branch/main/graph/badge.svg?token=WQLIP37828)](https://codecov.io/gh/Fifiuba/users-service)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Fifiuba/users-service/blob/develop/LICENSE)
[![Develop on Okteto](https://okteto.com/develop-okteto.svg)](https://backend-agustinaa235.cloud.okteto.net/)

### App

This is the users services used to handle all the request for the users. Some of these request are: create, update, read and delete a user.    

### Technologies 

#### Language & Libraries
* Version de python Python 3.8.5
* Version de poetry Poetry (version 1.2.0)
* Docker version 20.10.17
* Docker compose version 2.6.0


#### Data Base

* Postgres

#### External Services

* firebase : [link](https://console.firebase.google.com/u/0/project/user-service-9def8/overview)
* Okteto: [link](https://backend-agustinaa235.cloud.okteto.net/)
* codecov: [link](https://app.codecov.io/gh/Fifiuba/users-service)
* Datadog : [link](https://app.datadoghq.com/event/explorer?cols=&messageDisplay=expanded-lg&options=&sort=DESC&from_ts=1669555776832&to_ts=1670160576832&live=true)

### Developers

|Name                | Email                |
|--------------------|----------------------|
| Agustina Segura    | asegura@fi.uba.ar    |
| Alejo villores     | avillores@fi.uba.ar  |
| Maria Sol Fontela  | msfontenla@fi.uba.ar |

### Development 

#### Development Environment

* Instructions for installing tools
    * Poetry: [a link](https://python-poetry.org/docs/)
    * docker: [a link](https://docs.docker.com/compose/install/)

* Instructions to get the service running in a docker container
    *  Install all the tools use in the proyect
    * You will need to add a `.env` file. Use .env.example as guide 
    * To build and run the user service execute the following commands

        ```
        docker compose build
        docker compose up
        ```

    This will start the app's container. 
    * After stopping the execution, you must run

        ```
        docker compose down -v
        ```

    * You can also use build_network.sh to run the user service and to stop it use stop_netword.sh


### Project Structure
*
``` 
.
├──   .coverage
├──   .env.example
├──   .flake8
├──   .gitignore
├──   build.sh
├──   build_network.sh
├──   coverage.xml
├──   docker-compose.yml
├──   Dockerfile
├──  LICENSE
├──   logs.log
├──   poetry.lock
├──   pyproject.toml
├──   README.md
├──   stop_network.sh
├──   test.db
├──   test.sh
├───.github
│
│
├───tests
│   ├── app_test.py
│   └──   test_config.py
│   
│
└───users_service
    ├── app.py
    ├── main.py
    │   
    ├───controllers
    │   ├──user_controller.py 
    │
    ├───database
    │   ├── crud.py
    │   ├── database.py
    │   ├── exceptions.py
    │   ├── models.py
    │   ├── schema.py
    │   ├── user_repository.py
    │
    ├───utils
        ├── authorization_handler.py
        ├── events_generator.py
        ├── events_handler.py
        ├── events_mockup.py
        ├── firebase_handler.py
        ├── firebase_implementation.py
        ├── firebase_keys.json
        ├── firebase_mock.py
        ├── token_handler.py
```

* Arquitectura: [a link](https://lucid.app/lucidchart/2b0082b4-0986-4100-94b0-df16a620bc21/edit?invitationId=inv_221440e6-e888-4abd-a513-a07c1c196692&page=0_0#)

### Testing

* Steps to run the test
    ```bash
    poetry run pytest
    ```
### Run the APP
* Steps to run the app locally
    ```bash
    poetry install
    poetry run uvicorn users_service.app:app --reload
    ```

* Stepts to run the formatter
    ```bash
    poetry run black <carpeta>
    ```
* Steps to run the linter
    ```bash
    poetry run flake8 <carpeta>
    ```
### Deployment
To deploy the app:  
1. Connect [Okteto](https://www.okteto.com/) to your github account.
2. Go to the project folder
3. Run 
```
okteto deploy --build
```
