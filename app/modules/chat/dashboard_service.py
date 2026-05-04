from app.modules.chat.dashboard_repository import (
    listar_logs,
    listar_logs_sem_resposta,
    buscar_metricas,
    buscar_uso_por_dia,
    top_perguntas,
    ranking_intents,
    top_sem_resposta,
)


def get_logs(limit: int = 50, inicio: str | None = None, fim: str | None = None):
    return listar_logs(limit, inicio, fim)


def get_logs_sem_resposta(limit: int = 50, inicio: str | None = None, fim: str | None = None):
    return listar_logs_sem_resposta(limit, inicio, fim)


def get_metricas(inicio: str | None = None, fim: str | None = None):
    return buscar_metricas(inicio, fim)

def get_uso_por_dia(inicio: str | None = None, fim: str | None = None):
    return buscar_uso_por_dia(inicio, fim)

def get_top_perguntas(limit: int = 10, inicio: str | None = None, fim: str | None = None):
    return top_perguntas(limit=limit, inicio=inicio, fim=fim)


def get_ranking_intents(limit: int = 10, inicio: str | None = None, fim: str | None = None):
    return ranking_intents(limit=limit, inicio=inicio, fim=fim)


def get_top_sem_resposta(limit: int = 10, inicio: str | None = None, fim: str | None = None):
    return top_sem_resposta(limit=limit, inicio=inicio, fim=fim)