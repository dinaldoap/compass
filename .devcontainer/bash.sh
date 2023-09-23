#!/bin/bash

## Linux tools ##
# Clean bashrc and bash aliases configurations
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
code --install-extension ms-python.isort > /dev/null
# activate virtual environment
activate
# <<< devcontainer <<<
EOF
