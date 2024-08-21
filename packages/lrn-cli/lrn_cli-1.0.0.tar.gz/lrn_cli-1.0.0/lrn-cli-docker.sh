#!/bin/sh

realpath () {
    if [ -f "$1" ] ; then
        d="$(dirname $1)"
        f="$(basename $1)"
        echo "$(cd $d; pwd -P)/$f"
    fi
}

defer () {
    trap "$1" EXIT
}

VARS=$(mktemp /tmp/lrn-cli.env.XXX) || exit 1
defer "rm -f $VARS"
env | grep LRN_ | grep -v LRN_SHARED_CREDENTIALS_FILE | grep -v LRN_CONFIG_FILE > "$VARS"
CRED=$(realpath "${LRN_SHARED_CREDENTIALS_FILE:-${HOME}/.learnosity/credentials}")
CONF=$(realpath "${LRN_CONFIG_FILE:-${HOME}/.learnosity/config}")
docker container run -i --rm \
    -w /srv/local \
    --env-file="${VARS}" \
    --net host \
    -v "${CRED}:/root/.learnosity/credentials:ro" \
    -v "${CONF}:/root/.learnosity/config:ro" \
    -v "$(pwd):/srv/local" \
    "lrn-cli:${LRN_CLI_PKG_VER:-latest}" \
    "$@"
