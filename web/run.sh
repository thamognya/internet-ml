#!/bin/sh

concurrently "cd backend && ./manage.py runserver localhost:8080" "cd frontend && yarn build && yarn start"
