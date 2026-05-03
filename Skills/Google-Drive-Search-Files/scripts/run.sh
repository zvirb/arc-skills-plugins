#!/bin/bash
# Fixed: Use provided query and parent from lobster pipeline
/home/marku/.local/bin/gog drive ls --query "$1" --json
