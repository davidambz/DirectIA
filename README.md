# Projeto

Automação para envio de mensagens personalizadas via Instagram com base em perfis públicos.

O projeto utiliza Selenium para acessar perfis do Instagram, extrair informações como nome e bio, e a API da OpenAI (GPT) para gerar mensagens personalizadas com base nesses dados.

---

## 🚀 Funcionalidades

- Login automático no Instagram  
- Extração de nome, bio e link do perfil  
- Geração de mensagem personalizada com GPT  
- Envio automático da mensagem via DM  
- Ação opcional de seguir o perfil  
- Configurações flexíveis via `.env` com base no `.env-example`

---

## 🛠 Tecnologias usadas

- Python 3.12+  
- [Selenium](https://www.selenium.dev/)  
- [OpenAI Python SDK](https://pypi.org/project/openai/)  
- [Poetry](https://python-poetry.org/)  

---

## ⚙️ Como configurar

```bash
# Clone o repositório
git clone https://github.com/davidambz/thps.git
cd thps

# Instale o Poetry (caso ainda não tenha)
pip install poetry

# Instale as dependências
poetry install
```

---

## 🔑 Variáveis de ambiente (.env)

Crie um arquivo `.env` na raiz com base no `.env-example` incluído no projeto.

Exemplo de `.env`:

```env
INSTAGRAM_USER=seu_usuario
INSTAGRAM_PASS=sua_senha
OPENAI_API_KEY=sua_chave_openai

GPT_SYSTEM_PROMPT=Você é um especialista em comunicação.
GPT_USER_PROMPT=Sou alguém oferecendo um serviço personalizado e quero iniciar uma conversa educada e contextualizada.

USE_GPT=true
SEND_MESSAGES=false
```

---

## 📁 Estrutura do projeto

```bash
projeto/
├── src/
│   ├── main.py
│   ├── data/
│   │   └── profiles.txt         # Lista de usernames a processar
│   ├── handlers/
│   │   ├── file_handler.py
│   │   ├── instagram_handler.py
│   │   └── gpt_handler.py
├── .env
├── .env-example
├── README.md
└── pyproject.toml
```

---

## ▶️ Como usar

1. Adicione os nomes de usuários do Instagram no arquivo `src/data/profiles.txt`, um por linha.  
2. Configure seu `.env` com base no `.env-example`.  
3. Execute o projeto:

```bash
# Rodar em modo teste (sem envio e sem GPT)
poetry run python src/main.py
```

4. Para ativar o envio e a geração com GPT, configure no `.env`:

```env
USE_GPT=true
SEND_MESSAGES=true
```

O sistema acessa o perfil de cada usuário listado, extrai os dados, gera uma mensagem personalizada com até 300 caracteres e envia via DM (caso ativado).

---

## 🛡️ Avisos

- Use com responsabilidade. Automação no Instagram pode violar os termos da plataforma.
- Mantenha seu uso limitado e evite spam.