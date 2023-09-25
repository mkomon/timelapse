#!/bin/sh

case "$1" in
  "timelapse" )
    shift
    python3 timelapse.py $@
    ;;
  "bash" )
    echo dropping to shell "$1" - "$@"
    exec $@
    ;;
  * )
    exec $@
    ;;
esac
