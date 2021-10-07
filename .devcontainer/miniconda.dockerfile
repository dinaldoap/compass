FROM continuumio/miniconda3:4.10.3

# Install Linux tools
RUN apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
      openssh-client \
      git \
      build-essential \
      locales && \
    rm -rf /var/lib/apt/lists/*

RUN echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen && \
    locale-gen

# Config locale
ENV LC_ALL en_US.UTF-8

# Config standard user
ARG USERNAME=miniconda

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

# Config conda for rootless user mount
RUN mkdir --parents /opt/conda/pkgs && \
    chown -R ${USERNAME}:${USERNAME} /opt/conda/pkgs && \
    chown -R ${USERNAME}:${USERNAME} /opt/conda/envs

# Config pip cache for rootless user mount
RUN mkdir --parents "${HOME}/.cache/pip" && \
    chown -R ${USERNAME}:${USERNAME} "${HOME}/.cache/pip"

# Config workspace
RUN mkdir /workspace && \
    chown -R ${USERNAME}:${USERNAME} /workspace
    
# Set the default user
USER $USERNAME

# Set the default shell to bash instead of sh
ENV SHELL /bin/bash

# Install python dependencies
ADD --chown=miniconda:miniconda conda.yml /workspace/
ADD --chown=miniconda:miniconda requirements.txt /workspace/
ADD --chown=miniconda:miniconda setup.py /workspace/
RUN cd /workspace && \
    conda env create --file conda.yml && \
    conda clean --all && \
    pip cache purge && \    
    rm conda.yml && \
    rm requirements.txt && \
    rm setup.py

CMD ["/bin/bash"]