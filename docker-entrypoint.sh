#!/usr/bin/env bash

set -eou pipefail

exec gosu transformer \
  gunicorn \
      -w "$WORKERS" \
      -b "$ADDRESS:$PORT" \
      --access-logfile - \
      --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Forwarded-For}i)s"' \
      GenerateEmbedding:app
