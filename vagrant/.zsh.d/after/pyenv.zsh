if [ -e ~/.pyenv ]; then
  export PYENV_ROOT=~/.pyenv
  export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init -)"
  pyenv virtualenvwrapper_lazy
fi
