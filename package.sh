#!/bin/bash

pyinstaller compass/main.py --onefile --name compass \
                                    --exclude-module tkinter \
                                    --hidden-import cmath
#python setup.py bdist_wheel --universal