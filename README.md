# Servicio de Usuarios
---

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Fifiuba/users-service/Python%20application?label=build&style=flat-square&logo=GitHub)](https://github.com/Fifiuba/users-service/commits)
[![GitHub issues](https://img.shields.io/github/issues/Fifiuba/users-service?&style=flat-square)](https://github.com/Fifiuba/users-service/issues)
[![GitHub license](https://img.shields.io/github/license/Fifiuba/users-service?&style=flat-square)](https://github.com/Fifiuba/users-service/blob/main/LICENSE)

### Instalación

Version de python
```shell
python --version
Python 3.8.5
 ```
Version de poetry
```bash
poetry --version
Poetry (version 1.2.0)
 ```

Pasos para levantar el servidor local una vez clonado el repo
```bash
poetry install
poetry run uvicorn users_service.app:app --reload
```
