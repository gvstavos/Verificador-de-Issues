Criado por Gustavo Silva

# Verificador de Issues
## Descrição
Ferramenta criada para automatizar uma tarefa repetitiva e sujeita a erros: verificar manualmente issues concluídas quando o armazenamento da pasta de evidências de bugs da rede atinge o limite.
---
## Funcionalidades
- **Verificador de issues concluídas/verificadas** integrado com API do Jira.  
- **Renomeador automático de pastas**, para padronizar nomes no formato `XXX-0000` quando o usuário inserir apenas o número do ticket.  
- **Re-validador da verificação de issues concluídas**, garantindo que as issues apontadas como concluídas estejam realmente finalizadas.  
### Funcionalidade Extra
- **Armazenador de dados informados** (caminho da pasta, e-mail e token do Jira) para evitar retrabalho ao reabrir o programa.
---
## Tecnologia Utilizada
- Python
---
## Como rodar o projeto
Você pode executar o programa de duas formas:
1. **Usando o executável**:  
   Na pasta `dist` há um arquivo `.exe` pronto para uso, basta executá-lo diretamente.
2. **Rodando pelo código-fonte**:  
   Execute o arquivo `main.py` com o Python instalado na sua máquina.  
   ```bash
   python main.py
