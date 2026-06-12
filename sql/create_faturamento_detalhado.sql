CREATE TABLE IF NOT EXISTS fato_faturamento_associacao (
    data_chave integer NOT NULL,
    data_referencia date NOT NULL,
    departamento integer NOT NULL,
    associacao integer NOT NULL,
    atualizacao text,
    faturamento numeric(13,2),
    rep_faturamento numeric(13,2),
    projecao numeric(13,2),
    margem numeric(13,2),
    preco_medio numeric(13,2),
    ticket_medio numeric(13,2),
    meta_alcancada numeric(13,2),
    juros numeric(13,2),
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now(),
    PRIMARY KEY (data_chave, departamento, associacao)
);

CREATE TABLE IF NOT EXISTS fato_faturamento_filial (
    data_chave integer NOT NULL,
    data_referencia date NOT NULL,
    departamento integer NOT NULL,
    id_filial integer NOT NULL,
    atualizacao text,
    filial text,
    faturamento numeric(13,2),
    rep_faturamento numeric(13,2),
    projecao numeric(13,2),
    margem numeric(13,2),
    preco_medio numeric(13,2),
    ticket_medio numeric(13,2),
    meta_alcancada numeric(13,2),
    juros numeric(13,2),
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now(),
    PRIMARY KEY (data_chave, departamento, id_filial)
);

CREATE INDEX IF NOT EXISTS idx_fat_assoc_data
ON fato_faturamento_associacao (data_referencia);

CREATE INDEX IF NOT EXISTS idx_fat_assoc_departamento
ON fato_faturamento_associacao (departamento);

CREATE INDEX IF NOT EXISTS idx_fat_filial_data
ON fato_faturamento_filial (data_referencia);

CREATE INDEX IF NOT EXISTS idx_fat_filial_departamento
ON fato_faturamento_filial (departamento);

CREATE INDEX IF NOT EXISTS idx_fat_filial_id
ON fato_faturamento_filial (id_filial);
