#!/usr/bin/env bash

# SOURCE: https://github.com/apache/airflow/blob/669b026c0bed36572ff0c5ab2eaf3f6d2c845577/scripts/ci/ci_lint_dockerfile.sh

set -xeuo pipefail

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd ${MY_DIR}/../


docker run -v $(pwd)/Dockerfile:/root/Dockerfile -v $(pwd)/.hadolint.yaml:/root/.hadolint.yaml \
    -w /root hadolint/hadolint /bin/hadolint Dockerfile
