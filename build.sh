#!/bin/bash

# Ativa o ambiente virtual
source venv/bin/activate

# Executa o PyInstaller
pyinstaller --onefile src/gitai/gitai.py

# Copia o arquivo .env.example
cp .env.example dist/.env
