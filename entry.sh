#!bin/bash

# install uvicorn if not installed check the pipfile

if ! [ -x "$(command -v uvicorn)" ]; then
  echo 'Error: uvicorn is not installed.' >&2
  pip install uvicorn
fi