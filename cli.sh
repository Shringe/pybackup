#!/bin/sh

# Symlink this file to somewhere in your $PATH to access pybackup globally.
# example:
#   ln -s ~/path/of/this/file/cli.sh ~/.local/share/bin/pybackup

cd $(dirname $(realpath $0))
./venv/bin/python -m pybackup "$@"

