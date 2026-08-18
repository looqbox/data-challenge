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

Não commite o `.env` e não o inclua na entrega.

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

Não vamos passar o dicionário de dados. Levantar colunas, tipos e domínios faz
parte da questão.

### Entrega esperada

- A query.
- O resultado, com todas as regionais.
- Um parágrafo curto com as premissas adotadas.

---

## Questão 2: Python, reconstrução de estoque

### Enunciado

O time de suprimentos precisa saber **qual era o saldo de estoque de cada SKU em
cada loja, dia a dia**. O sistema de origem grava apenas as movimentações, e não
o saldo. Cabe a você reconstruir a curva diária a partir do histórico de
movimentos, e depois apontar quais séries não fecham.

Reconstrua o saldo **diário** por loja e SKU na janela de **2026-04-01 a
2026-07-31**, e valide o resultado. Escreva estas duas funções:

```python
def reconstruir_saldo(df: pd.DataFrame, dt_ini: str, dt_fim: str) -> pd.DataFrame:
    """Saldo diário por (loja, sku, dia).

    Todos os dias do intervalo devem estar preenchidos para cada célula,
    inclusive os dias sem nenhuma movimentação.
    """


def validar(saldo_df: pd.DataFrame) -> pd.DataFrame:
    """Aponta as células cuja série de saldo é implausível, com o
    diagnóstico de cada caso."""
```

### Fonte

Extraia o que precisar e traga para o pandas.

| Tabela                  | Conteúdo                 |
| ----------------------- | ------------------------ |
| `estoque_movimentacoes` | Movimentações de estoque |

### Entrega esperada

- O código das duas funções.
- O saldo reconstruído, em CSV.
- O retorno da `validar`, com quantas células foram apontadas e por qual
  diagnóstico.
- **3 linhas** explicando o que você faria com essas células.

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

- **Uma página** para o diretor, com a conclusão no primeiro parágrafo.
- As queries e o código que sustentam a análise.
- Uma seção **"o que eu não consigo afirmar com esses dados, e as 3 perguntas
  que eu faria antes da reunião"**. Cada pergunta deve ser uma que, respondida,
  mudaria a sua recomendação. Diga o que mudaria.

O último item vale 25% da nota do case sozinho. Não é preenchimento de
formulário.

---

## Stack

- MySQL 8, acesso por credencial enviada por e-mail
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
