#!/usr/bin/env bash
set -eu

cd "$(dirname "$0")"

BUILD_DIR="${1:-build}"

cmake -S . -B "$BUILD_DIR" -DCMAKE_BUILD_TYPE=Release
cmake --build "$BUILD_DIR" --config Release
ctest --test-dir "$BUILD_DIR" -C Release --output-on-failure