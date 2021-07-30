#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
tar -czvf pepys.tar.gz $SCRIPT_DIR/../src
cp $SCRIPT_DIR/pepys.spec ~/rpmbuild/SPECS
mv pepys.tar.gz ~/rpmbuild/SOURCES
rpmbuild -ba ~/rpmbuild/SPECS/pepys.spec