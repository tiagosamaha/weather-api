#!/bin/bash
# 
# Ubuntu Xenial install python3.x 

sudo apt-get update; sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libpq-dev git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

if [ ! -f ~/.pyenv/.git/refs/heads/master ]; then
  curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
fi

if ! [ -x "$(command -v pyenv)" ]; then
  sed -Ei -e '/^([^#]|$)/ {a \
  export PYENV_ROOT="$HOME/.pyenv"
  a \
  export PATH="$PYENV_ROOT/bin:$PATH"
  a \
  ' -e ':a' -e '$!{n;ba};}' ~/.bashrc
  echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
  echo 'eval "$(pyenv init -)"' >> ~/.bashrc

  # Set PATH for current subshell invocation
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init --path)"
  eval "$(pyenv init -)"
fi

if ! [[ $(python3 --version) == "Python 3.7.10" ]]; then
  # Install pythopn 3.7.10
  pyenv install 3.7.10
  # Set py37 as global python
  pyenv global 3.7.10
fi

sudo ln -s /usr/bin/python3.7 /usr/bin/python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py;
python3 get-pip.py --force-reinstall;
pip3 install virtualenv;
virtualenv -p python3 env1;
