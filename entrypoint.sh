#!/bin/bash

mode=$1
shift

if [[ "$mode" = "shell" ]]; then
    exec /bin/bash
elif [ "$mode" = "lint" ]; then
    exec ruff . --exclude=tests
elif [[ "$mode" = "test" ]]; then
    exec pytest -vv
elif [[ "$mode" = "dev" ]]; then
    exec uvicorn npb.app:app --host 0.0.0.0 --port 8000 --reload
else
    exec echo 'unknown command'
fi
