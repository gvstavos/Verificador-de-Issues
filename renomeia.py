import os
import re

def renomear_pastas(pasta_base, log_callback=None):
    """
    Renomeia pastas no formato AGRO3889 → AGRO-3889
    """
    padrao = re.compile(r"^([A-Za-z]+)(\d+)$")
    itens = os.listdir(pasta_base)

    for item in itens:
        caminho_antigo = os.path.join(pasta_base, item)

        if not os.path.isdir(caminho_antigo):
            continue

        match = padrao.match(item)
        if match:
            letras, numeros = match.groups()
            novo_nome = f"{letras}-{numeros}"
            caminho_novo = os.path.join(pasta_base, novo_nome)

            if not os.path.exists(caminho_novo):
                os.rename(caminho_antigo, caminho_novo)
                msg = f"Renomeado: {item} → {novo_nome}"
            else:
                msg = f"Já existe: {novo_nome}"

            if log_callback:
                log_callback(msg)
            else:
                print(msg)
