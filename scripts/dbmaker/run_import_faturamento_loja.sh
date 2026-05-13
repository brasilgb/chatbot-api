#!/bin/bash

cd /home/ia/projects/chatbot-api || exit 1

source .venv/bin/activate
source scripts/dbmaker/env_dbmaker.sh

python scripts/dbmaker/import_faturamento_total.py >> logs/import_faturamento_total.log 2>&1
python scripts/dbmaker/import_resumo_total.py >> logs/import_resumo_total.log 2>&1
