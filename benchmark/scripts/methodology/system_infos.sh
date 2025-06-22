#!/bin/bash

VARS_MK="$1"

if [ -z "$VARS_MK" ]; then
    echo "Usage: $0 <path_to_variables.mk>"
    exit 1
fi

get_var() {
    local var="$1"
    grep -E "^$var\s*=" "$VARS_MK" | sed -E "s/^$var\s*=\s*//" | head -n1
}

cat <<EOF
Compiler: $($(get_var "CXX") --version 2>/dev/null | head -n1)
CFLAGS: $(get_var "CFLAGS") $(get_var "RELEASE_CFLAGS")
LDFLAGS: $(get_var "LDFLAGS")

OS: $(lsb_release -ds 2>/dev/null || grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"')
Kernel: $(uname -r)
EOF
