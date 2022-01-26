#!/bin/bash

pip wheel --no-deps --wheel-dir dist .
#pyinstaller compass/__main__.py --onefile --name compass \
#                                    --exclude-module tkinter \
#                                    --hidden-import cmath \
#                                    --log-level ERROR