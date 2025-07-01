import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from dotenv import set_key
import threading
import subprocess

ENV_PATH = ".env"


def salvar_env(campo, valor):
    set_key(ENV_PATH, campo, valor)


def selecionar_arquivo():
    caminho = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")]
    )
    if caminho:
        salvar_env("PROFILE_FILE", os.path.basename(caminho))
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, os.path.basename(caminho))


def iniciar_processamento():
    botao_iniciar.config(state=tk.DISABLED)
    texto_logs.insert(tk.END, "\n⏳ Iniciando processamento...\n")

    def run():
        try:
            subprocess.run(["python", "src/main.py"], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", str(e))
        finally:
            botao_iniciar.config(state=tk.NORMAL)
            texto_logs.insert(tk.END, "\n✅ Finalizado.\n")

    threading.Thread(target=run).start()


def atualizar_env_e_salvar():
    salvar_env("INSTAGRAM_USER", entrada_user.get())
    salvar_env("INSTAGRAM_PASS", entrada_senha.get())
    salvar_env("OPENAI_API_KEY", entrada_api.get())
    salvar_env("GPT_USER_PROMPT", entrada_prompt.get())
    salvar_env("USE_GPT", str(var_gpt.get()))
    salvar_env("SEND_MESSAGES", str(var_enviar.get()))
    salvar_env("FOLLOW_USERS", str(var_seguir.get()))
    messagebox.showinfo("Salvo", "Configurações atualizadas.")


janela = tk.Tk()
janela.title("DirectIA - Interface")
janela.geometry("580x600")

# Campos principais
entrada_user = tk.Entry(janela, width=40)
entrada_senha = tk.Entry(janela, show="*", width=40)
entrada_api = tk.Entry(janela, width=40)
entrada_prompt = tk.Entry(janela, width=40)
entrada_arquivo = tk.Entry(janela, width=40)

var_gpt = tk.BooleanVar()
var_enviar = tk.BooleanVar()
var_seguir = tk.BooleanVar()

# Labels e entradas
campos = [
    ("Usuário Instagram:", entrada_user),
    ("Senha Instagram:", entrada_senha),
    ("Chave OpenAI:", entrada_api),
    ("Prompt personalizado:", entrada_prompt),
    ("Arquivo de perfis:", entrada_arquivo),
]

for i, (label, entry) in enumerate(campos):
    tk.Label(janela, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
    entry.grid(row=i, column=1, padx=10)

botao_arquivo = tk.Button(janela, text="Selecionar", command=selecionar_arquivo)
botao_arquivo.grid(row=4, column=2, padx=5)

# Checkboxes
tk.Checkbutton(janela, text="Usar GPT", variable=var_gpt).grid(row=5, column=0, sticky="w", padx=10, pady=10)
tk.Checkbutton(janela, text="Enviar mensagens", variable=var_enviar).grid(row=5, column=1, sticky="w")
tk.Checkbutton(janela, text="Seguir perfis", variable=var_seguir).grid(row=5, column=2, sticky="w")

# Botões
botao_salvar = tk.Button(janela, text="Salvar configurações", command=atualizar_env_e_salvar)
botao_salvar.grid(row=6, column=0, columnspan=2, pady=10)

botao_iniciar = tk.Button(janela, text="Iniciar", command=iniciar_processamento)
botao_iniciar.grid(row=6, column=2, pady=10)

# Área de logs
tk.Label(janela, text="Logs:").grid(row=7, column=0, sticky="nw", padx=10)
texto_logs = scrolledtext.ScrolledText(janela, width=70, height=20)
texto_logs.grid(row=8, column=0, columnspan=3, padx=10, pady=5)

janela.mainloop()
