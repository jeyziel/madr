#!/bin/bash 

poetry run alembic upgrade head

#Inicia Aplicação
poetry run uvicorn --host 0.0.0.0 --port 8000 madr.app:app