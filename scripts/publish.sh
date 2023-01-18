#!/bin/sh

poetry build
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
