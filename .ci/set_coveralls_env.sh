#!/bin/sh
# SOURCE: https://github.com/kaizhu256/codeaholics-hackathon/blob/7690f9ce8de58a48409a7e242cbffef58dea8db8/utility2.sh
# SOURCE: https://docs.coveralls.io/supported-ci-services
## init travis-ci.org env

echo " [debug] First lets see what we have for default environment variables. Running 'env | grep \"TRAVIS_\"'"
env | grep "TRAVIS_"

echo " [debug] First lets see what we have for default environment variables. Running 'env | grep \"CI_\"'"
env | grep "CI_"

echo " [debug] First lets see what we have for default environment variables. Running 'env | grep \"CI_\"'"
env | grep "COV_"

if [ "$TRAVIS" ]
then
  # INFO: https://docs.travis-ci.com/user/environment-variables/
  ## export $CI_BUILD_DIR
  export CI_BUILD_DIR=/build.travis-ci.org
  ## export TRAVIS_* vars as CI_* vars
  if [ ! "$CI_BRANCH" ]
  then
    export CI_BRANCH=$TRAVIS_BRANCH
  fi
  if [ ! "$CI_BUILD_NUMBER" ]
  then
    export CI_BUILD_NUMBER=$TRAVIS_BUILD_NUMBER
  fi
  if [ ! "$CI_COMMIT_ID" ]
  then
    export CI_COMMIT_ID=$TRAVIS_COMMIT
  fi
else
  export CI_BUILD_DIR=/build.local
fi
## export CI_* vars
if [ ! "$CI_BRANCH" ]
then
  export CI_BRANCH=$(git rev-parse --abbrev-ref HEAD)
fi
if [ ! "$CI_COMMIT_ID" ]
then
  export CI_COMMIT_ID=$(git rev-parse --verify HEAD)
fi
if [ ! "$CI_COMMIT_MESSAGE" ]
then
  export CI_COMMIT_MESSAGE=$(git log -1 --pretty=%s)
fi
if [ ! "$CI_COMMIT_INFO" ]
then
  export CI_COMMIT_INFO="$CI_COMMIT_ID - $CI_COMMIT_MESSAGE"
fi
export CI_BUILD_DIR_COMMIT=$CI_BUILD_DIR/$CI_BUILD_NUMBER.$CI_BRANCH.$CI_COMMIT_ID
export CI_BUILD_DIR_LATEST=$CI_BUILD_DIR/latest.$CI_BRANCH
## used in test report summary
export GITHUB_REPO_URL=https://github.com/$GITHUB_REPO/tree/$CI_BRANCH
