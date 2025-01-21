#!/bin/sh
set -e

uvicorn app.app:app --host 0.0.0.0 --port 8000 &

sleep 10

python ./populate_db.py

wait $!