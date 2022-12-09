#!/bin/sh

export FLASK_APP=./ersystestapi/main.py

poetry run flask --app 'ersystestapi:main' --debug run -h 0.0.0.0
