#!/usr/bin/env bash
set -e

CERTS_DIR="./$(dirname $0)/../certs"

cd $CERTS_DIR
./gen-certs.sh
