#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec "$SCRIPT_DIR/run_imports_via_docker.sh" \
    import_faturamento_detalhado.py \
    import_faturamento_total.py \
    import_resumo_total.py
