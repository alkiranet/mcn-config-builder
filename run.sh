#!/bin/bash

# is python3 installed?
check_python3_installed() {
    if ! command -v python3 &> /dev/null
    then
        echo "Python 3 is not installed. Please install it to continue."
        exit 1
    fi
}

# which version?
check_python_version() {
    PYTHON_VERSION=$(python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')
    if [ "$PYTHON_VERSION" \< "3.0" ]; then
        echo "Python 3 is required. Found Python $PYTHON_VERSION."
        exit 1
    fi
}

# is installed?
check_python3_installed

# is version?
check_python_version

# run
CONFIG_FILE=${1:-"./networks.cnf"}
python3 -m bin.run_generator "$CONFIG_FILE"