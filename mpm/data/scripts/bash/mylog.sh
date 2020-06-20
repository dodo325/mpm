#!/bin/bash
# Обёртка для вывода логов в терминал
_time=$(date +"%T.%3N")
mylog_info() { echo -e "\e[0;40;36m($_time)[*] $@ \e[0m"; }
mylog_success() { echo -e "\e[1;40;92m($_time)[ok] $@ \e[0m"; }
mylog_warning() { echo -e "\e[0;40;33m($_time)[warn] $@ \e[0m"; }
mylog_debug() { echo -e "($_time)[ ] $@"; }
mylog_error() { echo -e "\e[1;40;91m($_time)[fail] $@ \e[0m"; }


main() {
    mylog_info "info"
    mylog_success "success"
    mylog_warning "warning"
    mylog_debug "debug"
    mylog_error "error"
}

if [ "${1}" != "--source-only" ]; then
    main "${@}"
fi

