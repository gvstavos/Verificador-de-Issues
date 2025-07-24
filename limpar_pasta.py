import os
import requests

def verificar_issues_concluidas(pasta_base, usuario, token, output_file="issues_concluidas.txt", log_callback=None):
    """
    Verifica pastas na pasta_base, consulta o status das issues no Jira e salva as concluídas em um arquivo.

    :param pasta_base: Caminho da pasta com as subpastas nomeadas pelas issues
    :param usuario: Usuário (e-mail) para autenticação no Jira
    :param token: Token de autenticação no Jira
    :param output_file: Nome do arquivo para salvar as issues concluídas
    :param log_callback: Função para exibir logs (opcional, ex.: integração com GUI)
    :return: Lista de issues concluídas
    """
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

    log("Iniciando verificação das issues concluídas...")

    if not os.path.isdir(pasta_base):
        raise ValueError(f"A pasta {pasta_base} não existe!")

    itens = os.listdir(pasta_base)
    pastas = [item for item in itens if os.path.isdir(os.path.join(pasta_base, item))]
    jira_api_base = "https://realtec.atlassian.net/rest/api/2/issue/"
    issues_concluidas = []

    log(f"Diretório base: {pasta_base}")
    log(f"Encontradas {len(pastas)} pastas para verificar.")

    for codigo in pastas:
        log(f"Processando pasta: {codigo}")

        # Ajustar código da issue se necessário
        if "-" not in codigo and not any(c.isalpha() for c in codigo):
            codigo = f"AGRO-{codigo}"
            log(f"Código ajustado para: {codigo}")

        url = jira_api_base + codigo
        log(f"Consultando URL: {url}")

        response = requests.get(url, auth=(usuario, token))

        if response.status_code == 200:
            dados = response.json()
            status = dados['fields']['status']['name']
            log(f"Status da issue {codigo}: {status}")

            if status.lower() in ["concluído", "concluída","verificado","verificada"]:
                issues_concluidas.append(codigo)
                log(f"Issue {codigo} está concluída/verificada.")
        else:
            msg = f"Erro ao consultar {codigo}: {response.status_code}"
            log(msg)

    # Salvar no arquivo
    if issues_concluidas:
        log(f"Salvando {len(issues_concluidas)} issues concluídas em {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            for issue in issues_concluidas:
                f.write(issue + "\n")
        log("Arquivo salvo com sucesso.")
    else:
        log("Nenhuma issue concluída encontrada.")

    log("Verificação finalizada.")
    return issues_concluidas
