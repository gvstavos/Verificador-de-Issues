import requests
import os

def revalidar_issues(arquivo_issues, usuario, token, projeto_default="AGRO", output_file="issues_inconsistentes.txt", log_callback=None):
    """
    Revalida issues listadas em um arquivo, consultando o Jira para verificar status atual.

    :param arquivo_issues: Caminho do arquivo TXT com as issues (uma por linha)
    :param usuario: Usuário Jira (e-mail)
    :param token: Token Jira
    :param projeto_default: Prefixo padrão (caso issue no TXT esteja só com número)
    :param output_file: Nome do arquivo para salvar inconsistências
    :param log_callback: Função para exibir logs (opcional)
    :return: Lista de inconsistências [(issue, status_atual), ...]
    """
    if not os.path.isfile(arquivo_issues):
        raise FileNotFoundError(f"Arquivo {arquivo_issues} não encontrado!")

    jira_api_base = "https://realtec.atlassian.net/rest/api/2/issue/"

    # Lê as issues do arquivo
    with open(arquivo_issues, "r", encoding="utf-8") as f:
        issues = [linha.strip() for linha in f if linha.strip()]

    inconsistencias = []

    if log_callback:
        log_callback("\n=== Revalidando status no Jira ===\n")
    else:
        print("\n=== Revalidando status no Jira ===\n")

    for issue_key in issues:
        # Ajusta formato: se não tiver hífen e nenhuma letra, adiciona prefixo padrão
        if "-" not in issue_key and not any(c.isalpha() for c in issue_key):
            issue_key = f"{projeto_default}-{issue_key}"

        url = jira_api_base + issue_key
        response = requests.get(url, auth=(usuario, token))

        if response.status_code == 200:
            dados = response.json()
            status = dados['fields']['status']['name']

            if status.lower() in ["concluído", "concluída"]:
                msg = f"{issue_key}: ✅ Continua concluída"
            else:
                msg = f"{issue_key}: ❌ NÃO está concluída (status atual: {status})"
                inconsistencias.append((issue_key, status))

            if log_callback:
                log_callback(msg)
            else:
                print(msg)
        else:
            msg = f"Erro ao consultar {issue_key}: {response.status_code}"
            if log_callback:
                log_callback(msg)
            else:
                print(msg)

    # Salva inconsistências em arquivo
    if inconsistencias:
        with open(output_file, "w", encoding="utf-8") as f:
            for issue, status in inconsistencias:
                f.write(f"{issue} - Status atual: {status}\n")
        if log_callback:
            log_callback(f"\nRelatório salvo: {output_file} ({len(inconsistencias)} inconsistências encontradas)")
        else:
            print(f"\nRelatório salvo: {output_file} ({len(inconsistencias)} inconsistências encontradas)")
    else:
        if log_callback:
            log_callback("\nTodas as issues continuam concluídas ✅")
        else:
            print("\nTodas as issues continuam concluídas ✅")

    return inconsistencias
