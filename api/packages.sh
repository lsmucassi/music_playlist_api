#!/bin/bash

# Exit if any command fails
set -aux pipefail

pip install -t lib -r requirements.txt
(cd lib; zip ../lambda_function.zip -r .)
zip lambda_function.zip -u main.py

# clean files
rm -rf lib