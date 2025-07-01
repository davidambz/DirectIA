import os
import subprocess
from tkinter import filedialog, StringVar, BooleanVar
import ttkbootstrap as tb
from ttkbootstrap.constants import *

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")

class DirectIAInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("DirectIA")
        self.style = tb.Style("superhero")

        self.fields = {
            "Usuário do Instagram": StringVar(),
            "Senha do Instagram": StringVar(),
            "Chave da OpenAI": StringVar(),
            "Resumo do comportamento da IA": StringVar(),
        }

        self.user_prompt_text = None
        self.use_gpt = BooleanVar()
        self.send_messages = BooleanVar()
        self.follow_users = BooleanVar()
        self.selected_file_path = ""
        self.selected_file_label = None

        self._create_widgets()

    def _create_widgets(self):
        container = tb.Frame(self.root, padding=20)
        container.pack(fill=BOTH, expand=True)

        for label_text, var in self.fields.items():
            tb.Label(container, text=label_text).pack(anchor="w", pady=(10, 0))
            entry_show = "*" if "Senha" in label_text else ""
            tb.Entry(container, textvariable=var, show=entry_show).pack(fill=X)

        tb.Label(container, text="Mensagem de apresentação").pack(anchor="w", pady=(10, 0))
        self.user_prompt_text = tb.Text(container, height=4)
        self.user_prompt_text.pack(fill=BOTH, pady=(0, 10))

        tb.Checkbutton(container, text="Usar inteligência artificial", variable=self.use_gpt).pack(anchor="w")
        tb.Checkbutton(container, text="Enviar mensagens automaticamente", variable=self.send_messages).pack(anchor="w")
        tb.Checkbutton(container, text="Seguir perfis automaticamente", variable=self.follow_users).pack(anchor="w")

        tb.Button(container, text="Selecionar lista de perfis", command=self.select_profile_file).pack(anchor="w", pady=(15, 0))
        self.selected_file_label = tb.Label(container, text="Nenhum arquivo selecionado", font=("Arial", 8, "italic"))
        self.selected_file_label.pack(anchor="w", pady=(2, 10))

        tb.Button(container, text="Iniciar", bootstyle="success", command=self._save_and_run).pack(fill=X, pady=(20, 0))

    def select_profile_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Arquivos de texto", "*.txt *.csv")]
        )
        if file_path:
            self.selected_file_path = file_path
            file_name = os.path.basename(file_path)
            self.selected_file_label.config(text=f"Arquivo selecionado: {file_name}")

    def _save_and_run(self):
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.write(f"INSTAGRAM_USER={self.fields['Usuário do Instagram'].get()}\n")
            f.write(f"INSTAGRAM_PASS={self.fields['Senha do Instagram'].get()}\n")
            f.write(f"OPENAI_API_KEY={self.fields['Chave da OpenAI'].get()}\n")
            f.write(f"GPT_SYSTEM_PROMPT={self.fields['Resumo do comportamento da IA'].get()}\n")
            f.write(f"GPT_USER_PROMPT={self.user_prompt_text.get('1.0', 'end').strip()}\n")
            f.write(f"USE_GPT={'true' if self.use_gpt.get() else 'false'}\n")
            f.write(f"SEND_MESSAGES={'true' if self.send_messages.get() else 'false'}\n")
            f.write(f"FOLLOW_USERS={'true' if self.follow_users.get() else 'false'}\n")

        env = os.environ.copy()
        env["PROFILES_FILE"] = self.selected_file_path
        subprocess.Popen(["python", "src/main.py"], env=env)

if __name__ == "__main__":
    root = tb.Window()
    app = DirectIAInterface(root)
    root.mainloop()
