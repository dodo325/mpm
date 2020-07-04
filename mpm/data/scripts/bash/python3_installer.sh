#!/bin/bash
# 
# 
# 
_lb="\e[0;40;36m"
_lg="\e[1;40;92m"
_ly="\e[1;40;93m"
_lr="\e[1;40;91m"
_ld="\e[1;40m"
_e="\e[0m"
_time=$(date +"%T.%3N")
log_info()    { echo -e "$_lb($_time)[INFO] $@ $_e"; }
log_success() { echo -e "$_lg($_time)[ OK ] $@ $_e"; }
log_warning() { echo -e "$_ly($_time)[warn] $@ $_e"; }
log_debug()   { echo -e "$_ld($_time)[    ] $@ $_e"; }
log_error()   { echo -e "$_lr($_time)[FAIL] $@ $_e"; }



check_python3() {
    log_info "Check Python3"
    PYTHON3_COMMANDS=$(compgen -c | grep "^python3")

    if [ -z "$PYTHON3_COMMANDS" ]; then
        log_warning "Not found Python3"
    else
        PYTHON3_VER=$(python3 -c "import sys; print(sys.version_info >= (3, 7))")
        if [ "$PYTHON3_VER" != "True" ]; then
            log_error "Python3 not 3.7"
            # return -1;
            exit 0;
        fi
        log_success "Detect python3"
        exit 0;
    fi
}
aptget_install_from_ppa(){
    log_debug "Use deadsnakes ppa"
    sudo apt-get install software-properties-common -y
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt-get update
    sudo apt-get install python3.7 python3-pip -y
}
pacman_install(){ # archlinux
    sudo pacman -S python;
    sudo pacman -S python-pip;
}
aptget_install(){
    log_debug "Use apt-get"
    __registry_verion=$(apt-cache show python3 | grep -oE "Version: 3.[7-9]" | awk '{print tolower($0)}')
    if [ ! -z "$__registry_verion" ]; then
        log_info "Detect in registry python3 $__registry_verion" 
        sudo apt-get install python3 python3-pip -y;
    else
        aptget_install_from_ppa;
    fi
    check_python3;
}
main() {
    # check_python3;
    if [ "$OSTYPE" = cygwin ]; then
		log_error "Python >=3.7 is not supported in this script for Cygwin"
		exit 1
	fi

    log_info "Install Python3..."
    __apt=$(compgen -c | grep "^apt-get")
    if [ ! -z "$__apt" ]; then
        aptget_install;
    fi
    
    __pacman=$(compgen -c | grep "^pacman")
    if [ ! -z "$__pacman" ]; then
        pacman_install;
    fi
}

if [ "${1}" != "--source-only" ]; then
    main "${@}"
fi