# Looqbox Data Challenge

Solução completa do desafio técnico da Looqbox, cobrindo SQL Test, Cases 1–3 e geração de relatório PDF consolidado.

---

## Pré-requisitos

- Python 3.10+
- Acesso à rede com as credenciais do banco fornecidas pela Looqbox
- Git

---

## Instalação

```bash
# 1. Clone o repositório (após fazer o fork)
git clone https://github.com/SEU_USUARIO/data-challenge.git
cd data-challenge

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```bash
cp .env.example .env
```

Preencha com as credenciais recebidas por e-mail:

```env
DB_HOST=35.199.115.174
DB_USER=looqbox-challenge
DB_PASSWORD=looq-challenge
DB_NAME=looqbox_challenge
```

> O arquivo `.env` está no `.gitignore` e nunca será versionado.

---

## Estrutura do projeto

```
data-challenge/
│
├── cases/
│   ├── __init__.py
│   ├── sql_test.py         # SQL Test — Q1, Q2, Q3
│   ├── case1.py            # Função dinâmica retrieve_data
│   ├── case2.py            # Ticket Médio por loja (Q4 2019)
│   └── case3.py            # Análise e visualização IMDB
│
├── config/
│   ├── __init__.py
│   └── database.py         # Conexão MySQL via variáveis de ambiente
│
├── data/
│   └── sql/                # Arquivos .sql das queries
│
├── outputs/                # PDFs e imagens gerados (ignorado pelo git)
│
├── utils/
│   └── generate_report.py  # Gerador de PDF com identidade Looqbox
│
├── .env                    # Credenciais locais (não versionado)
├── .env.example            # Modelo de variáveis de ambiente
├── .gitignore
├── logo.png                # Logo Looqbox (usada na capa do PDF)
├── main.py                 # Ponto de entrada — executa tudo
├── requirements.txt
└── README.md
```

---

## Execução

Com o ambiente virtual ativado e o `.env` configurado, rode:

```bash
python looqbox_challenge.py
```

Isso executa em sequência:

1. **SQL Test** — três queries contra o banco Looqbox
2. **Case 1** — demonstração da função `retrieve_data`
3. **Case 2** — cálculo do Ticket Médio e geração do gráfico
4. **Case 3** — análise IMDB e geração das visualizações
5. **PDF** — relatório consolidado salvo em `outputs/looqbox_report.pdf`

---

## Cases

### SQL Test

Três queries respondendo:

- **Q1** — 10 produtos mais caros (`ORDER BY PRODUCT_VAL DESC LIMIT 10`)
- **Q2** — Seções dos departamentos BEBIDAS e PADARIA
- **Q3** — Vendas totais por Business Area no Q1 2019

### Case 1 — `retrieve_data`

Função dinâmica que aceita filtros opcionais e constrói a query em tempo de execução:

```python
from cases.case1 import retrieve_data

# Sem filtros — retorna tudo
df = retrieve_data()

# Com filtros combinados
df = retrieve_data(
    product_code=301409,
    store_code=3,
    date=["2019-01-01", "2019-03-31"],
)
```

Todos os parâmetros são opcionais. Parâmetros ausentes são simplesmente ignorados na cláusula `WHERE`.

### Case 2 — Ticket Médio

- Usa as duas queries do cliente **sem modificação**
- Filtro de período `['2019-10-01', '2019-12-31']` aplicado em Python
- Ticket Médio calculado como `SALES_VALUE / SALES_QTY` por loja
- Gráfico de barras horizontal salvo em `outputs/case2_ticket_medio.png`

### Case 3 — IMDB

- **Violin plot** de notas por década: revela a distribuição completa, não apenas a média — evidenciando o viés de sobrevivência de filmes antigos
- **Bar chart horizontal** dos top 10 gêneros por nota média (mínimo 20 filmes)
- Imagens salvas em `outputs/`

---

## Dependências principais

| Pacote | Uso |
|---|---|
| `mysql-connector-python` | Conexão com o banco MySQL |
| `pandas` | Manipulação de dados |
| `matplotlib` | Gráficos |
| `seaborn` | Violin plot e estilização |
| `reportlab` | Geração do PDF |
| `Pillow` | Processamento da logo no PDF |
| `python-dotenv` | Leitura do `.env` |
