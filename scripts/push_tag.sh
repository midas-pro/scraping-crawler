#!/bin/bash

VERSION=$(head -n 1 lncrawl/VERSION)

# git push --delete origin "v$VERSION"
# git tag -d "v$VERSION"
git tag "v$VERSION"
git push --tags
