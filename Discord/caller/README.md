# Discord Caller Bot

Bot de exemplo para Discord usando `discord.py` e variáveis de ambiente.

## Configuração

1. Crie e ative um ambiente virtual:
   - Windows (PowerShell): `python -m venv .venv`\n`.\.venv\Scripts\Activate.ps1`
   - Windows (CMD): `python -m venv .venv`\n`.\.venv\Scripts\activate.bat`

2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` com base em `.env.example`:
   ```bash
   copy .env.example .env
   ```

4. Preencha `DISCORD_TOKEN` no arquivo `.env`.

## Uso

Inicie o bot com:
```bash
python caller.py
```

## Comandos

- `!ping` — responde `Pong! 🏓`
- `!hello` — envia uma saudação ao autor da mensagem

## Estrutura

- `caller.py` — ponto de entrada do bot
- `.env.example` — exemplo de configuração de ambiente
- `.gitignore` — arquivos e pastas ignorados pelo Git
- `.github/workflows/python-app.yml` — workflow do GitHub Actions
- `.vscode/` — configuração do VS Code

## Observações

Não faça commit do `.env` real. O token do bot deve ser mantido em segredo.
