#!/bin/bash

pyinstaller --onefile src/gitai/gitai.py

cp .env.example dist/.env