#!/bin/bash
pip install pyinstaller
pyinstaller --onefile --name PRIMEXARMY PRIMEXARMY.py
echo "✅ Build complete! Binary is in dist/PRIMEXARMY"
