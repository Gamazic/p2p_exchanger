#!/usr/bin/env bash

set -e

HOST="$1"

openssl genrsa -out cert.pem 2048 &&\
  openssl req -new -x509 -days 365 -key cert.pem -out pubkey.pem -subj "/CN=${HOST}"
