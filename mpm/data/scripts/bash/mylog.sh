#!/bin/bash
# Обёртка для вывода логов в терминал
_time=$(date +"%T.%3N")

_e="\e[0m"
_r="\e[1;49;91m"
_o="\e[1;49;93m"
_g="\e[1;49;32m"
_p="\e[0;49;95m"

_lb="\e[0;40;36m"
_lg="\e[1;40;92m"
_ly="\e[1;40;93m"
_lr="\e[1;40;91m"
_ld="\e[1;40m"
log_info()    { echo -e "$_lb($_time)[INFO] $@ $_e"; }
log_success() { echo -e "$_lg($_time)[ OK ] $@ $_e"; }
log_warning() { echo -e "$_ly($_time)[warn] $@ $_e"; }
log_debug()   { echo -e "$_ld($_time)[    ] $@ $_e"; }
log_error()   { echo -e "$_lr($_time)[FAIL] $@ $_e"; }


main() {
    log_info "info"
    log_success "success"
    log_warning "warning"
    log_debug "debug"
    log_error "error"
}

if [ "${1}" != "--source-only" ]; then
    main "${@}"
fi