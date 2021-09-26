#!/bin/bash

# This script requires a virtual env (save time pulling down deps everytime)

# pip install virtualenvwrapper
# mkvirtualenv githook-prov
# source /usr/local/bin/virtualenvwrapper.sh
# mkvirtualenv githook-prov
workon githook-prov

# the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# the temp directory used, within $DIR
# omit the -p parameter to create a temporal directory in the default location
WORK_DIR=`mktemp -d -p /tmp`

# check if tmp dir was created
if [[ ! "$WORK_DIR" || ! -d "$WORK_DIR" ]]; then
  echo "Could not create temp dir"
  exit 1
fi

# deletes the temp directory
function cleanup {      
  rm -rf "$WORK_DIR"
  echo "Deleted temp repo $WORK_DIR"
}

# register the cleanup function to be called on the EXIT signal
trap cleanup EXIT

# echo $DIR
# echo $WORK_DIR
mkdir "$WORK_DIR"/repo && cd "$_"
git init
git config --global user.email "jdoe@example.com"
git config --global user.name "John Doe"

cp "$DIR"/pre-commit.py "$WORK_DIR"/repo/.git/hooks/pre-commit
chmod +x "$WORK_DIR"/repo/.git/hooks/pre-commit
cp "$DIR"/sigstore_pycode.py "$WORK_DIR"/repo/.git/hooks/sigstore_pycode.py

FOO=$(mktemp "$WORK_DIR"/repo/foo.XXXXXXXXX)
BAR=$(mktemp "$WORK_DIR"/repo/bar.XXXXXXXXX)

# Set up a basic git repo with something in it!
git add $FOO 
git commit --allow-empty -n -m "Initial commit."

# Replicate a developer making a commit
git add $BAR
git commit -m "Sigstore commmit"
sleep 100