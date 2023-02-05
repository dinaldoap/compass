#!/bin/bash

# Clean bashrc and bash aliases configurations
sed --in-place --expression '/# >>> venv-init >>>/,/*# <<< venv-init <<</d' ~/.bashrc ~/.bash_aliases

# Config bash aliases
cat << EOF >> ~/.bash_aliases
# >>> venv-init >>>
# current folder virtual environment activation
alias activate="source .venv/bin/activate"
# <<< venv-init <<<
EOF

# Config bashrc
cat << EOF >> ~/.bashrc
# >>> venv-init >>>
cd $(pwd)
# activate virtual environment
activate
# <<< venv-init <<<
EOF
