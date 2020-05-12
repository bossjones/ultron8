#!/usr/bin/env bash

TRAVIS_BASE_URL=https://travis-ci.org
GITHUB_BASE_URL=https://github.com
# run this before package-artifact.sh.  Said script will add it to the deploy artifact
touch digest.yml

# git link
echo "# Diff for branch" > digest.yml
echo "git_diff_url: ${GITHUB_BASE_URL}/${TRAVIS_REPO_SLUG}/compare/${TRAVIS_COMMIT_RANGE}" >> digest.yml
echo "git_pr_number: ${TRAVIS_PULL_REQUEST}" >> digest.yml
echo "git_pr_url: ${GITHUB_BASE_URL}/${TRAVIS_REPO_SLUG}/pull/${TRAVIS_PULL_REQUEST}" >> digest.yml
echo "# Tag for commit (if it exists)" >> digest.yml
echo "git_tag: ${TRAVIS_TAG}" >> digest.yml
# CI Link
echo "# CI link for build" >> digest.yml
echo "ci_build_url: ${TRAVIS_BASE_URL}/${TRAVIS_REPO_SLUG}/builds/${TRAVIS_BUILD_ID}" >> digest.yml
echo "ci_build_number: ${TRAVIS_JOB_NUMBER}" >> digest.yml

echo "contents of digest.yml: "
cat digest.yml
