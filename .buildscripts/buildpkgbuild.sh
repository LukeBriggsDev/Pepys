#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
GZIP=-n tar -czvf pepys.tar.gz $SCRIPT_DIR/../src
makepkg
rm pepys.tar.gz
rm -r pkg
rm -r src