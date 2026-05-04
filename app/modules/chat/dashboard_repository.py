from sqlalchemy import text
from app.core.database import SessionLocal


def listar_logs(limit: int = 50, inicio: str | None = None, fim: str | None = None):
    db = SessionLocal()

    try:
        where = ""
        params = {"limit": limit}

        if inicio and fim:
            where = "WHERE created_at::date BETWEEN :inicio AND :fim"
            params["inicio"] = inicio
            params["fim"] = fim

        result = db.execute(
            text(f"""
                SELECT id, pergunta, intent, resposta, sucesso, created_at
                FROM chat_logs
                {where}
                ORDER BY id DESC
                LIMIT :limit
            """),
            params,
        )

        return [dict(row._mapping) for row in result.fetchall()]

    finally:
        db.close()


def listar_logs_sem_resposta(
    limit: int = 50, inicio: str | None = None, fim: str | None = None
):
    db = SessionLocal()

    try:
        where = "WHERE sucesso = false"
        params = {"limit": limit}

        if inicio and fim:
            where += " AND created_at::date BETWEEN :inicio AND :fim"
            params["inicio"] = inicio
            params["fim"] = fim

        result = db.execute(
            text(f"""
                SELECT id, pergunta, intent, resposta, sucesso, created_at
                FROM chat_logs
                {where}
                ORDER BY id DESC
                LIMIT :limit
            """),
            params,
        )

        return [dict(row._mapping) for row in result.fetchall()]

    finally:
        db.close()


def buscar_metricas(inicio: str | None = None, fim: str | None = None):
    db = SessionLocal()

    try:
        where = ""
        params = {}

        if inicio and fim:
            where = "WHERE created_at::date BETWEEN :inicio AND :fim"
            params["inicio"] = inicio
            params["fim"] = fim

        total = db.execute(
            text(f"SELECT COUNT(*) FROM chat_logs {where}"),
            params,
        ).scalar()

        sucesso = db.execute(
            text(
                f"SELECT COUNT(*) FROM chat_logs {where + (' AND' if where else 'WHERE')} sucesso = true"
            ),
            params,
        ).scalar()

        falhas = db.execute(
            text(
                f"SELECT COUNT(*) FROM chat_logs {where + (' AND' if where else 'WHERE')} sucesso = false"
            ),
            params,
        ).scalar()

        return {
            "total_perguntas": total,
            "total_sucesso": sucesso,
            "total_falhas": falhas,
        }

    finally:
        db.close()


def buscar_uso_por_dia(inicio: str | None = None, fim: str | None = None):
    db = SessionLocal()

    try:
        where = ""
        params = {}

        if inicio and fim:
            where = "WHERE created_at::date BETWEEN :inicio AND :fim"
            params["inicio"] = inicio
            params["fim"] = fim

        result = db.execute(
            text(f"""
                SELECT
                    created_at::date AS data,
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE sucesso = true) AS sucesso,
                    COUNT(*) FILTER (WHERE sucesso = false) AS falhas
                FROM chat_logs
                {where}
                GROUP BY created_at::date
                ORDER BY data ASC
            """),
            params,
        )

        return [dict(row._mapping) for row in result.fetchall()]

    finally:
        db.close()

from sqlalchemy import text
from app.core.database import SessionLocal


def top_perguntas(limit: int = 10, inicio: str | None = None, fim: str | None = None):
    db = SessionLocal()

    try:
        where = ""
        params = {"limit": limit}

        if inicio and fim:
            where = "WHERE created_at::date BETWEEN :inicio AND :fim"
            params["inicio"] = inicio
            params["fim"] = fim

        result = db.execute(
            text(f"""
                SELECT 
                    pergunta,
                    COUNT(*) AS total
                FROM chat_logs
                {where}
                GROUP BY pergunta
                ORDER BY total DESC
                LIMIT :limit
            """),
            params,
        )

        return [dict(row._mapping) for row in result.fetchall()]

    finally:
        db.close()


def ranking_intents(limit: int = 10, inicio: str | None = None, fim: str | None = None):
    db = SessionLocal()

    try:
        where = ""
        params = {"limit": limit}

        if inicio and fim:
            where = "WHERE created_at::date BETWEEN :inicio AND :fim"
            params["inicio"] = inicio
            params["fim"] = fim

        result = db.execute(
            text(f"""
                SELECT 
                    COALESCE(intent->>'tipo', 'sem_intent') AS intent,
                    COUNT(*) AS total
                FROM chat_logs
                {where}
                GROUP BY COALESCE(intent->>'tipo', 'sem_intent')
                ORDER BY total DESC
                LIMIT :limit
            """),
            params,
        )

        return [dict(row._mapping) for row in result.fetchall()]

    finally:
        db.close()

def top_sem_resposta(limit: int = 10, inicio: str | None = None, fim: str | None = None):
    db = SessionLocal()

    try:
        where = "WHERE sucesso = false"
        params = {"limit": limit}

        if inicio and fim:
            where += " AND created_at::date BETWEEN :inicio AND :fim"
            params["inicio"] = inicio
            params["fim"] = fim

        result = db.execute(
            text(f"""
                SELECT 
                    pergunta,
                    COUNT(*) AS total
                FROM chat_logs
                {where}
                GROUP BY pergunta
                ORDER BY total DESC
                LIMIT :limit
            """),
            params,
        )

        return [dict(row._mapping) for row in result.fetchall()]

    finally:
        db.close()