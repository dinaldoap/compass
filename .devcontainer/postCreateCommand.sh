#!/bin/bash

if [ ! -d .venv ]; then
    make venv
fi
make venv-init
