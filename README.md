# Análise de transações

Script simples para executar as etapas do exercício.

Instale as bibliotecas:

```bash
pip install -r requirements.txt
```

Gere os arquivos e execute a análise:

```bash
python gerar_dados.py
python app.py
```

O gráfico abre em uma janela. Os resultados das tabelas aparecem no terminal.

Para entregar, publique `app.py`, `gerar_dados.py` e `requirements.txt` em um repositório no GitHub.

## Publicar no GitHub

Crie um repositório vazio no GitHub. Depois, execute nesta pasta, substituindo a URL pela do seu repositório:

```bash
git init
git add app.py gerar_dados.py requirements.txt README.md
git commit -m "Cria painel de análise de transações"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```