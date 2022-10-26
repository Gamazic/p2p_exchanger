#!/usr/bin/env bash
set -e

CERTS_DIR="./../certs"

cd $CERTS_DIR
$CERTS_DIR/gen-certs.sh
