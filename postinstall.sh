#!/bin/bash

# Caminho para o Python do sistema
PYTHON_PATH=/usr/bin/python3

# Caminho para o pip do sistema
PIP_PATH=/usr/bin/pip3

# Caminho para o arquivo requirements.txt
REQUIREMENTS_PATH=requirements.txt

# Verifica se o Python 3 está instalado
if ! command -v $PYTHON_PATH &> /dev/null
then
    echo "Python 3 não está instalado. Por favor, instale o Python 3 e tente novamente."
    exit 1
fi

# Verifica se o pip está instalado
if ! command -v $PIP_PATH &> /dev/null
then
    echo "pip não está instalado. Por favor, instale o pip e tente novamente."
    exit 1
fi

# Instala as bibliotecas Python necessárias
$PYTHON_PATH -m pip install -r $REQUIREMENTS_PATH