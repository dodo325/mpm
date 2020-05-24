#!/bin/bash
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
. $SCRIPTPATH/mylog.sh --source-only

mylog_info "Check Python3"

PYTHON3=0
PYTHON3_COMMANDS=$(compgen -c | grep "^python3")

if [ -z "$PYTHON3_COMMANDS" ]; then
      mylog_warning "Not found Python3"
else
    PYTHON3_VER=$(python3 -c "import sys; print(sys.version_info >= (3, 7))")
    if [ "$PYTHON3_VER" != "True" ]; then
        mylog_error "Python3 not 3.7"
        # return -1;
        exit;
    fi
    mylog_success "Detect python3"
    exit;
fi

mylog_info "Install Python3..."

__apt=$(compgen -c | grep "^apt-get")
if [ ! -z "$__apt" ]; then
    mylog_debug "Use apt-get"
    sudo apt-get install software-properties-common -y
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt-get update
    sudo apt-get install python3.7 python3-pip -y
    mylog_success "Installed Python3"
    exit
fi