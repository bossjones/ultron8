#!/bin/bash
echo "================================================="
echo "pyenv versions: $(pyenv versions)"
echo "================================================="

echo 'export PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

echo 'export PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"' | sudo tee -a /etc/profile.d/developer.sh
echo 'eval "$(pyenv init -)"' | sudo tee -a /etc/profile.d/developer.sh
echo 'eval "$(pyenv virtualenv-init -)"' | sudo tee -a /etc/profile.d/developer.sh
