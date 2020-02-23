if [ -e /usr/local/rbenv ]; then
  export PATH="/usr/local/rbenv/shims:$PATH"
fi
if [[ -x $(which -p rbenv) ]]; then
  eval "$(rbenv init -)"
fi
