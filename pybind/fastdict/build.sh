#!/bin/bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pybind11
mkdir -p build
cd build
cmake ..
cmake --build .
cd ..
