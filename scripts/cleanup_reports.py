import os
import time

PASTA = "storage/reports"
TEMPO_LIMITE = 60 * 60  # 1 hora


def log(msg: str):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def limpar_imagens_antigas():
    if not os.path.exists(PASTA):
        log(f"Pasta não encontrada: {PASTA}")
        return

    agora = time.time()
    removidos = 0

    for arquivo in os.listdir(PASTA):
        caminho = os.path.join(PASTA, arquivo)

        if not os.path.isfile(caminho):
            continue

        idade = agora - os.path.getmtime(caminho)

        if idade > TEMPO_LIMITE:
            os.remove(caminho)
            removidos += 1
            log(f"Removido: {arquivo}")

    log(f"Limpeza finalizada. Arquivos removidos: {removidos}")


if __name__ == "__main__":
    limpar_imagens_antigas()