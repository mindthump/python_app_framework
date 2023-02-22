#!/bin/bash

# Startup commands, etc. go here
sudo chown 1000:1000 /data

# Run CMD, usually a shell (e.g., /bin/zsh)
exec "$@"
