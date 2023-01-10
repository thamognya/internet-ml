#!/bin/sh

concurrently "cd backend && ./manage.py runserver 0.0.0.0:8080" "cd frontend && yarn build && yarn start"
