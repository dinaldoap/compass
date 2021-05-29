#!/bin/bash

python setup.py bdist_wheel --universal --quiet
pyinstaller compass/__main__.py --onefile --name compass \
                                    --exclude-module tkinter \
                                    --hidden-import cmath \
                                    --log-level ERROR