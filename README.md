# Desafio Técnico Looqbox

Repositório com as soluções do desafio técnico Looqbox: questões SQL e cases em Python para consulta, agregação e visualização de dados em MySQL.

## O que foi realizado

### Questões SQL

Arquivo [`Questões SQL`](Questões%20SQL):

- **Top 10 produtos mais caros** — consulta à tabela `data_product` ordenada por `PRODUCT_VAL DESC`, limitada a 10 registros.
- **Seções de BEBIDAS e PADARIA** — `DISTINCT SECTION_NAME` filtrando por `DEP_NAME` nos dois departamentos.
- **Vendas do 1º trimestre de 2019 por Business Area** — join entre `data_product_sales` e `data_store_cad`, com soma de `SALES_VALUE` agrupada por `BUSINESS_NAME`.

### Case 1 — Consulta via terminal

Arquivo [`Case_1.py`](Case_1.py):

- Consulta `data_product_sales` filtrada por código do produto, código da loja e intervalo de datas.
- Entrada interativa no terminal com validação de inteiros e datas (formato DD-MM-AAAA).
- Conexão MySQL via PyMySQL, com credenciais lidas do arquivo `.env`.

### Case 1 Turbo — Interface gráfica

Arquivo [`Case_1_turbo.py`](Case_1_turbo.py):

- Mesma consulta do Case 1, com interface em tkinter.
- Comboboxes populadas com valores distintos do banco (produto e loja).
- Calendário para seleção de datas e tabela de resultados na tela.

> A interface gráfica foi desenvolvida com auxílio de IA.

### Case 2 — Join e agregação em pandas

Arquivo [`Case_2.py`](Case_2.py):

- Executa duas queries SQL fixas (cadastro de lojas e vendas de 2019), sem alteração no SQL.
- Tratamento 100% em pandas: conversão de tipos, inner join por `STORE_CODE`, filtro de outubro a dezembro de 2019.
- Agregação por loja, cálculo do TM (ticket médio = soma de `SALES_VALUE` / soma de `SALES_QTY`) com arredondamento half-up.
- Saída no terminal: `STORE_NAME`, `BUSINESS_NAME`, `TM`.

### Case 3 — Gráficos IMDB

Arquivo [`Case_3_graficos_lado_a_lado.py`](Case_3_graficos_lado_a_lado.py):

- Carga da tabela `IMDB_movies`, limpeza de tipos e explode de gêneros.
- Imagem única com dois gráficos lado a lado:
  - Dispersão rating médio × receita média por ano (com linha de tendência).
  - Área empilhada dos 6 gêneros mais comuns + linha de rating médio, com legenda externa.
- Resultado salvo em `analise_imdb/charts/case3_graficos_lado_a_lado.png`.

## Pré-requisitos e configuração

- Python 3
- Dependências em [`requirements.txt`](requirements.txt): PyMySQL, python-dotenv, pandas, matplotlib, seaborn
- Copiar [`.env.example`](.env.example) para `.env` e preencher as credenciais do MySQL

Instalação das bibliotecas:

```bash
pip install -r requirements.txt
```

Ou execute [`REVISAR_instalar_todos_cases.bat`](REVISAR_instalar_todos_cases.bat).

## Como executar

| Script | Comando / atalho |
|--------|------------------|
| Case 1 (terminal) | `python Case_1.py` ou `iniciar_Case_1.bat` |
| Case 1 Turbo (GUI) | `python Case_1_turbo.py` |
| Case 2 | `python Case_2.py` |
| Case 3 | `python Case_3_graficos_lado_a_lado.py` ou `iniciar_Case_3.bat` |
| Teste de conexão | `python "Teste Banco conectar.py"` |

## Estrutura do projeto

```
Looqbox/
├── Questões SQL
├── Case_1.py
├── Case_1_turbo.py
├── Case_2.py
├── Case_3_graficos_lado_a_lado.py
├── Teste Banco conectar.py
├── requirements.txt
├── .env.example
├── REVISAR_instalar_todos_cases.bat
├── iniciar_Case_1.bat
├── iniciar_Case_1_turbo.bat
├── iniciar_Case_3.bat
└── analise_imdb/charts/          # saída gerada pelo Case 3
```

---

*Este README foi redigido com auxílio de inteligência artificial.*
