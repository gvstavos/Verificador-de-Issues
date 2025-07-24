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
    if not os.path.isdir(pasta_base):
        raise ValueError(f"A pasta {pasta_base} não existe!")

    itens = os.listdir(pasta_base)
    pastas = [item for item in itens if os.path.isdir(os.path.join(pasta_base, item))]
    jira_api_base = "https://realtec.atlassian.net/rest/api/2/issue/"
    issues_concluidas = []

    if log_callback:
        log_callback(f"\n=== Verificando status das issues na pasta {pasta_base} ===\n")
    else:
        print(f"\n=== Verificando status das issues na pasta {pasta_base} ===\n")

    for codigo in pastas:
        if "-" not in codigo and not any(c.isalpha() for c in codigo):
            codigo = f"AGRO-{codigo}"
            
        url = jira_api_base + codigo
        response = requests.get(url, auth=(usuario, token))

        if response.status_code == 200:
            dados = response.json()
            status = dados['fields']['status']['name']

            if status.lower() in ["concluído", "concluída"]:
                issues_concluidas.append(codigo)
                if log_callback:
                    log_callback(f"Issue {codigo} está concluída.")
                else:
                    print(f"Issue {codigo} está concluída.")
        else:
            msg = f"Erro ao consultar {codigo}: {response.status_code}"
            if log_callback:
                log_callback(msg)
            else:
                print(msg)

    # Salvar no arquivo
    if issues_concluidas:
        with open(output_file, "w", encoding="utf-8") as f:
            for issue in issues_concluidas:
                f.write(issue + "\n")

    return issues_concluidas