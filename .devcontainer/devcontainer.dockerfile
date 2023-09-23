FROM python:3.11.0-bullseye

# Set the default shell to bash instead of sh
ENV SHELL /bin/bash

# Install Linux tools
RUN apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
      openssh-client \
      git \
      build-essential \
      bash-completion \
      locales && \
    rm -rf /var/lib/apt/lists/*

# Install NodeJS, NPM and prettier
RUN MAJOR=$(curl -i https://github.com/nodejs/node/releases/latest | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | sed -E 's/v([0-9]+)\.[0-9]+\.[0-9]+/\1/p' | tail -n 1) && \
    curl -fsSL https://deb.nodesource.com/setup_${MAJOR}.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
      nodejs && \
    rm -rf /var/lib/apt/lists/* && \
    npm install --global --save-dev --save-exact prettier

RUN echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen && \
    locale-gen

# Config locale
ENV LC_ALL en_US.UTF-8

# Config time zone
RUN ln --symbolic --force /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

# Config standard user
ARG USERNAME=user

# Or your actual UID, GID on Linux if not the default 1000
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    #
    # [Optional] Add sudo support
    apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq sudo && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME && \
    rm -rf /var/lib/apt/lists/*

# Technically optional
ENV HOME /home/$USERNAME

# Config VS Code server directory for rootless user mount
RUN mkdir "${HOME}/.vscode-server" && \
  chown -R ${USERNAME}:${USERNAME} "${HOME}/.vscode-server"

# Config cache directory for rootless user
RUN mkdir --parents "${HOME}/.cache" && \
    chown -R ${USERNAME}:${USERNAME} "${HOME}/.cache"

# Config workspace
RUN mkdir /workspace && \
    chown -R ${USERNAME}:${USERNAME} /workspace

# Set the default user
USER $USERNAME

CMD ["/bin/bash"]