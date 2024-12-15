cd /app

echo 1. Installing dependencies

pipenv install

echo 2. Creating files for worker nodes

pipenv requirements > requirements.txt

zip -r worker_files.zip *

echo 3. Running server

pipenv run uvicorn main:app --host ${BE_BINDING_HOST} --port ${BE_PORT} --reload