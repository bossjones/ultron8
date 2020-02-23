if [ -d "/usr/local/go/bin" ]; then
  export PATH=/usr/local/go/bin:$PATH
fi
export PATH=$GOPATH/bin:$PATH
alias cdgo='CDPATH=.:$GOPATH/src/github.com:$GOPATH/src/golang.org:$GOPATH/src'
