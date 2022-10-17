#!/bin/bash

mkdir --parents build && \
cat requirements.lock | grep '^\w' > build/constraints.lock && \
pip wheel --constraint=build/constraints.lock --no-deps --wheel-dir=dist .
#pyinstaller compass/__main__.py --onefile --name compass \
#                                    --exclude-module tkinter \
#                                    --hidden-import cmath \
#                                    --log-level ERROR