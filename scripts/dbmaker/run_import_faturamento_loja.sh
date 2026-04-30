#!/bin/bash

cd /home/ia/projects/chatbot-api || exit 1

source .venv/bin/activate
source scripts/dbmaker/env_dbmaker.sh

python scripts/dbmaker/import_faturamento_loja.py >> logs/import_faturamento_loja.log 2>&1
