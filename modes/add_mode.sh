#!/bin/bash

rm -rf $1
mkdir -p $1/config
cat <<EOF > $1/config/$1.yaml
# config_version=3

mode:
  start_events: $1_selected
  priority: 100
EOF