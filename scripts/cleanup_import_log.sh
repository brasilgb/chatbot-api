#!/bin/bash

LOG="/home/ia/projects/chatbot-api/logs/import_faturamento_diario.log"

if [ -f "$LOG" ]; then
    echo "" > "$LOG"
fi
