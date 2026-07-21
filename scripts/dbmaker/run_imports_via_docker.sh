#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

IMAGE="${ETL_IMAGE:-chatbot-etl_dbmaker}"
NETWORK="${ETL_NETWORK:-chatbot_chatbot_network}"

run_import() {
    local script_name="$1"

    docker run --rm \
        --network "$NETWORK" \
        --env-file "$PROJECT_ROOT/backend/.env" \
        -e PYTHONPATH=/app \
        -e DBMAKER=/home/dbmaker/5.4 \
        -e DBMAKER_HOME=/home/dbmaker/5.4 \
        -e DM_HOME=/home/dbmaker/5.4 \
        -e DB_DBDIR=/home/dbmaker/5.4 \
        -e ODBCINI=/etc/odbc.ini \
        -e ODBCSYSINI=/etc \
        -e LD_LIBRARY_PATH=/home/dbmaker/5.4/lib/so:/usr/lib64 \
        -e DB_NLS=/home/dbmaker/5.4/shared \
        -e DB_LOCALE=en \
        -e DB_CODEPAGE=Latin1 \
        -e DB_CLILCODE=1 \
        -e DB_CLIOCODE=1 \
        -e DB_LCODE=1 \
        -v "$PROJECT_ROOT/backend:/app" \
        -v "$PROJECT_ROOT/logs:/app/logs" \
        -v "$PROJECT_ROOT/storage:/app/storage" \
        -v /etc/odbc.ini:/etc/odbc.ini:ro \
        -v /etc/odbcinst.ini:/etc/odbcinst.ini:ro \
        -v /home/dbmaker/5.4:/home/dbmaker/5.4:rw \
        "$IMAGE" \
        sh -lc "ln -sf /home/dbmaker/5.4/lib/so/libiconv.so /libiconv.so && cd /app && PYTHONPATH=/app python3 scripts/dbmaker/$script_name"
}

if [ "$#" -gt 0 ]; then
    for script_name in "$@"; do
        run_import "$script_name"
    done
else
    run_import import_faturamento_detalhado.py
    run_import import_faturamento_total.py
    run_import import_resumo_total.py
fi
