#!/bin/bash
set -e # sets fast fail: immediately exit on any error

rm -f hoplitekb.oxt
mkdir -p build
cp -r src/* build
cd build
zip -r ../hoplitekb.oxt .
cd ..
rm -rf build
