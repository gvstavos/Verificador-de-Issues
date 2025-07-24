import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
import json
CONFIG_FILE = "config.json"
import threading

# Importando funções
from renomeia import renomear_pastas
from limpar_pasta import verificar_issues_concluidas
from validador import revalidar_issues

# === Função para exibir logs na interface ===
def log(msg):
    text_log.insert(tk.END, msg + "\n")
    text_log.see(tk.END)

# === Escolher pasta ===
def escolher_pasta():
    pasta = filedialog.askdirectory()
    entry_pasta.delete(0, tk.END)
    entry_pasta.insert(0, pasta)

def salvar_config():
    config = {
        "pasta": entry_pasta.get(),
        "email": entry_email.get(),
        "token": entry_token.get()
    }
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        log("💾 Configurações salvas com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro ao salvar", f"Erro ao salvar config: {e}")


def apagar_config():
    # Se o arquivo config.json existir, remove
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    
    # Limpa os campos da interface
    entry_pasta.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_token.delete(0, tk.END)
    
    log("⚠️ Configurações apagadas!")

def carregar_config():
    if os.path.exists(CONFIG_FILE):  # Só tenta abrir se existir
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                entry_pasta.insert(0, config.get("pasta", ""))
                entry_email.insert(0, config.get("email", ""))
                entry_token.insert(0, config.get("token", ""))
        except json.JSONDecodeError:
            print("⚠️ Arquivo de configuração inválido. Ele será recriado ao salvar.")


# === Executa renomeação ===
def executar_renomeacao():
    pasta = entry_pasta.get()
    if not os.path.isdir(pasta):
        messagebox.showerror("Erro", "Selecione uma pasta válida!")
        return
    renomear_pastas(pasta, log_callback=log)
    log("✅ Renomeação concluída!\n")

# === Executa verificação no Jira ===
def executar_verificacao():
    pasta = entry_pasta.get()
    usuario = entry_email.get().strip()
    token = entry_token.get().strip()

    if not all([os.path.isdir(pasta), usuario, token]):
        messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
        return

    # Mostrar loading
    lbl_status.config(text="🔍 Verificando issues, aguarde...")
    root.update_idletasks()

    # Rodar em uma thread separada
    def tarefa():
        issues = verificar_issues_concluidas(pasta, usuario, token, log_callback=log)

        # Quando terminar, atualizar a interface
        lbl_status.config(text=f"✅ Verificação concluída! {len(issues)} issues salvas.")
        root.update_idletasks()

    thread = threading.Thread(target=tarefa)
    thread.start()


# === Revalidar TXT ===
def executar_revalidacao():
    usuario = entry_email.get().strip()
    token = entry_token.get().strip()

    if not all([usuario, token]):
        messagebox.showerror("Erro", "Preencha usuário e token!")
        return

    arquivo = "issues_concluidas.txt"
    if not os.path.isfile(arquivo):
        messagebox.showerror("Erro", "Arquivo issues_concluidas.txt não encontrado!")
        return

    inconsistencias = revalidar_issues(arquivo, usuario, token, log_callback=log)
    log(f"\n✅ Revalidação concluída! {len(inconsistencias)} inconsistências encontradas.\n")

# === Interface Tkinter ===
root = tk.Tk()
root.title("Validador de Issues Jira")

lbl_status = tk.Label(root, text="", fg="blue", font=("Arial", 10))
lbl_status.pack(pady=5)

# Frame de configurações
frame_config = tk.Frame(root)
frame_config.pack(pady=10)

# Campo Pasta
tk.Label(frame_config, text="Pasta Base:").grid(row=0, column=0, padx=5, pady=5)
entry_pasta = tk.Entry(frame_config, width=40)
entry_pasta.grid(row=0, column=1, padx=5)
btn_browse = tk.Button(frame_config, text="Selecionar", command=escolher_pasta)
btn_browse.grid(row=0, column=2, padx=5)

# Campo Email
tk.Label(frame_config, text="E-mail Jira:").grid(row=1, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_config, width=40)
entry_email.grid(row=1, column=1, padx=5, columnspan=2)

# Campo Token
tk.Label(frame_config, text="Token Jira:").grid(row=2, column=0, padx=5, pady=5)
entry_token = tk.Entry(frame_config, width=40, show="*")
carregar_config()
entry_token.grid(row=2, column=1, padx=5, columnspan=2)

# Botões
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn_salvar = tk.Button(root, text="Salvar Configurações", command=salvar_config)
btn_salvar.pack(pady=5)

btn_apagar = tk.Button(root, text="Apagar Configurações", command=apagar_config)
btn_apagar.pack(pady=5)

btn_renomear = tk.Button(btn_frame, text="1) Renomear Pastas", width=25, command=executar_renomeacao)
btn_renomear.grid(row=0, column=0, padx=5)

btn_verificar = tk.Button(btn_frame, text="2) Verificar Issues (Salvar TXT)", width=25, command=executar_verificacao)
btn_verificar.grid(row=0, column=1, padx=5)

btn_revalidar = tk.Button(btn_frame, text="3) Revalidar TXT no Jira", width=25, command=executar_revalidacao)
btn_revalidar.grid(row=0, column=2, padx=5)

# Área de Log
text_log = scrolledtext.ScrolledText(root, width=90, height=20)
text_log.pack(pady=10)

root.mainloop()
