### Would you like to work with us? Apply [here](https://looqbox.gupy.io/)!

# Looqbox Data Challenge
![Looqbox](https://github.com/looqbox/data-challenge/blob/master/logo.png)

## Teste técnico: Analista de Dados / BI

## Acesso ao banco

**As credenciais são enviadas por e-mail**, junto com o convite.

| Variável         | Conteúdo             |
| ---------------- | -------------------- |
| `TT_DB_HOST`     | Endereço do servidor |
| `TT_DB_USER`     | Seu usuário          |
| `TT_DB_PASSWORD` | Sua senha            |

As tabelas das três questões estão no schema `looqbox-challenge-bi`.

---

## Questão 1: SQL

### Enunciado

A diretoria comercial acompanha a performance das regionais contra a meta do
mês. Você precisa entregar a consulta que alimenta esse acompanhamento.

Escreva **uma query** que retorne, por **regional**, referente a **julho de
2026**:

1. faturamento líquido
2. ticket médio
3. peças por atendimento (PA)
4. atingimento de meta
5. variação de faturamento contra julho de 2025, considerando **apenas mesmas
   lojas**

Ordene do maior gap absoluto contra a meta para o menor.

### Fonte

O histórico cobre julho de 2025 e julho de 2026.

| Tabela       | Conteúdo                       |
| ------------ | ------------------------------ |
| `dim_loja`   | Cadastro de lojas              |
| `fato_venda` | Movimento de venda, nível item |
| `fato_meta`  | Meta por filial                |

### Entrega esperada

- A query desenvolvida.
- O resultado, com todas as regionais.
- Um parágrafo curto com as premissas adotadas.

---

## Questão 2a: Python, reconstrução da curva diária

### Enunciado

O time de suprimentos precisa saber **qual era o saldo de estoque de cada SKU em
cada loja, dia a dia**. O sistema de origem grava apenas as movimentações, e não
o estoque em si. Cabe a você reconstruir a curva diária a partir do histórico de
movimentos, e depois apontar se há inconsistências físicas.

Reconstrua o saldo **diário** por loja e SKU na janela de **2026-04-01 a
2026-07-31**, usando **apenas** o que está em `movimentacoes`, e valide o
resultado. Escreva estas duas funções:

```python
def reconstruir_saldo(...) -> pd.DataFrame:
    """Saldo diário por (loja, sku, dia).

    Todos os dias do intervalo devem estar preenchidos para cada célula,
    inclusive os dias sem nenhuma movimentação.
    """

```

### Fonte

| Tabela                  | Conteúdo                 |
| ----------------------- | ------------------------ |
| `movimentacoes` | Movimentações de estoque |

### Entrega esperada

- O código utilizado para extrair e tratar os dados.
- O saldo reconstruído, em CSV.

---

## Questão 2b: Python, fechamento do período

### Enunciado

Suprimentos conseguiu a **contagem física do dia 2026-04-01**: a foto do estoque
no primeiro dia da janela, loja a loja e SKU a SKU. Ela não está no banco, veio
em planilha. Com ela na mão, a pergunta vira outra: **qual é o estoque no dia
2026-07-14?**

```python
def gerar_estoque_dia(...) -> pd.DataFrame:
    """Estoque por (loja, sku), partindo da foto de 2026-04-01."""
```

### Fonte

Duas fontes, em lugares diferentes. Elas não cobrem exatamente o mesmo conjunto
de células: decida o que fazer com quem aparece só de um lado, e registre a
decisão.

| Fonte                       | Onde está                            | Conteúdo                                     |
| --------------------------- |--------------------------------------| -------------------------------------------- |
| `estoque_foto_inicial.csv`  | arquivo no repositório               | Contagem física por loja e SKU em 01/04/2026 |
| `movimentacoes`             | banco, schema `looqbox-challenge-bi` | Movimentações de estoque              |

### Entrega esperada

- O código da função.
- Um **CSV** `estoque_20260714.csv` com as colunas `loja`, `sku`, `qtd`.
- Responda brevemente: existe alguma inconsistência nas bases apresentadas? Se 
sim, quais seriam e quais suas possíveis causas?

---

## Questão 3: Case

### Enunciado

> O ticket médio da rede caiu 8,2% em julho contra junho. O diretor comercial
> quer saber o motivo na reunião de segunda-feira, e quer uma recomendação.

Faça o caminho completo: extraia o que precisar, analise e comunique.

### Fonte

O histórico cobre junho e julho de 2026.

| Tabela                   | Conteúdo                          |
| ------------------------ | --------------------------------- |
| `case_vendas_cupom`      | Venda consolidada por cupom       |
| `case_dim_categoria`     | Cadastro de categorias            |
| `case_dim_loja_campanha` | Participação na campanha de julho |

### Entrega esperada

- **Uma página** para o diretor, com a conclusão no primeiro parágrafo e, ao menos, uma visualização.
- As queries e o código que sustentam a análise.
- Uma seção **"o que eu não consigo afirmar com esses dados, e as 3 perguntas
  que eu faria antes da reunião"**. Cada pergunta deve ser uma que, respondida,
  mudaria a sua recomendação. Diga o que mudaria.

---

## Stack

- SQL, acesso por credencial enviada por e-mail
- Python 3.11 ou superior
- **pandas como biblioteca principal de manipulação de dados**

Python puro é aceito onde fizer sentido. Não aceitamos polars, PySpark, Dask ou
qualquer engine distribuída: o volume aqui é pequeno de propósito, e o que se
avalia é o seu raciocínio sobre o dado, não a sua escolha de engine.

Para gráficos, use a biblioteca que preferir.

---

## Como entregar

**Por e-mail**, respondendo o e-mail do convite. Dois arquivos:

1. Um **PDF** com o código e os resultados de cada questão. É esse arquivo que
   vamos ler. A organização é escolha sua, e conta.
2. Um **zip** com os arquivos de código e as saídas geradas.

Não inclua o `.env` nem credenciais.

**Não abra pull request e não faça fork deste repositório.** Entrega via git é
pública: expõe as suas respostas para os outros candidatos e anula a sua
avaliação.

Prazo: 5 dias corridos a partir do e-mail de convite.

---

## Orientações

- Sempre que o enunciado for ambíguo, decida e registre a premissa. Premissa
  declarada vale ponto. Premissa escondida no código custa ponto.
- Preferimos uma entrega menor e validada a uma entrega completa e não
  conferida. Se faltar tempo, corte escopo e diga o que cortou.
- Se algo travar no acesso ao banco, responda o e-mail do convite. Tempo perdido
  em configuração de ambiente não conta contra você.

---

## Links úteis

- [Documentação do pandas](https://pandas.pydata.org/docs/)
- [Data Visualization Catalogue](https://datavizcatalogue.com/)
- [Guia de estilo PEP 8](https://peps.python.org/pep-0008/)
