#!/bin/bash

## Linux tools ##
# Clean bashrc and bash aliases configurations
touch ~/.bash_aliases
sed --in-place --expression '/# >>> devcontainer >>>/,/*# <<< devcontainer <<</d' ~/.bashrc ~/.bash_aliases

# Config bash aliases
cat << EOF >> ~/.bash_aliases
# >>> devcontainer >>>
# current folder virtual environment activation
alias activate="source .venv/bin/activate"
# <<< devcontainer <<<
EOF

# Config bashrc
cat << EOF >> ~/.bashrc
# >>> devcontainer >>>
# activate virtual environment
activate
# <<< devcontainer <<<
EOF
