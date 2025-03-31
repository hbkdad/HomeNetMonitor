#!/bin/bash

CONFIG_PATH="/usr/local/home-net-monitor/config.json"
HOST="localhost"

if [ -f "$CONFIG_PATH" ]; then
  REMOTE=$(jq -r '.remote_dashboard' "$CONFIG_PATH")
  if [ "$REMOTE" = "yes" ]; then
    HOST="0.0.0.0"
  fi
fi

cd /usr/local/home-net-monitor/frontend
HOST=$HOST npm start
