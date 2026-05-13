from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class ResumoTotalBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None

    data_chave: int | None = None
    data_referencia: date | None = None
    departamento: int | None = None

    atualizacao: str | None = None

    meta: Decimal | None = None
    faturamento: Decimal | None = None
    projecao: Decimal | None = None
    margem: Decimal | None = None
    preco_medio: Decimal | None = None
    ticket_medio: Decimal | None = None
    meta_alcancada: Decimal | None = None

    faturamento_sem_brasil: Decimal | None = None
    margem_sem_brasil: Decimal | None = None
    preco_medio_sem_brasil: Decimal | None = None

    venda_agora: Decimal | None = None
    venda_dia: Decimal | None = None

    margem_media_ano: Decimal | None = None
    juros_medio_ano: Decimal | None = None
    juros: Decimal | None = None
    juro_agora: Decimal | None = None


class ResumoPeriodoResponse(BaseModel):
    departamento: int | None = None
    data_inicio: date | None = None
    data_fim: date | None = None

    meta: Decimal | None = None
    faturamento: Decimal | None = None
    faturamento_sem_brasil: Decimal | None = None
    venda_agora: Decimal | None = None
    venda_dia: Decimal | None = None
    juro_agora: Decimal | None = None


class EvolucaoFaturamentoResponse(BaseModel):
    data_referencia: date | None = None
    departamento: int | None = None

    faturamento: Decimal | None = None
    meta: Decimal | None = None
    projecao: Decimal | None = None
    margem: Decimal | None = None
    meta_alcancada: Decimal | None = None
    venda_agora: Decimal | None = None
    venda_dia: Decimal | None = None


class MetaVsRealizadoResponse(BaseModel):
    data_referencia: date | None = None
    departamento: int | None = None

    meta: Decimal | None = None
    faturamento: Decimal | None = None
    projecao: Decimal | None = None
    meta_alcancada: Decimal | None = None