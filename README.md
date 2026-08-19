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
## Questão 2: Reconstrução de estoque

### A) Saldo diário

O time de suprimentos precisa saber **qual o saldo de estoque de cada SKU em
cada loja, dia a dia**. O sistema de origem grava apenas as movimentações, e não
o saldo. Cabe a você reconstruir a curva diária a partir do histórico de
movimentos.

Construa o saldo **diário** por loja e SKU na janela de **2026-04-01 a
2026-07-31**, e valide o resultado. 

| Tabela | Conteúdo |
|---|---|
| `movimentacoes` | Movimentações de produtos |

- Salve o resultado em um arquivo CSV: chamado saldo_diario.csv;

### B) Reconstruo o estoque
Após alguns dias da sua entrega, o estagiário da área encontrou um arquivo csv com
o estoque por loja e SKU do dia 2026-07-31. Apartir desse csv, você deve reconstruir
o estoque diário do período de 2026-04-01 a 2026-07-31.

- Utilize apenas Python para essa tarefa;
- O retorno deve ser um arquivo csv chamado: estoque_diario.csv;
- Aponte possíveis inconsistências nos dados encontrados;

---

## Questão 3: Análise de resultados

### Cenário

> O ticket médio da rede caiu 8,2% em julho contra junho. O diretor comercial
> quer saber o motivo na reunião de segunda-feira, e quer uma recomendação.

### Dados

| Tabela | Conteúdo |
|---|---|
| `case_vendas_cupom` | Venda consolidada por cupom |
| `case_dim_categoria` | Cadastro de categorias |
| `case_dim_loja_campanha` | Participação na campanha de julho |

### Entregas esperadas

- Monte um conjunto de visualizações (gráficos, tabelas, etc.) que auxiliem o diretor
entender as causas dessa queda no indicador, mostrando para ele os principais 
ofensores e demais informações relevantes para a análise;
- Grave um vídeo de no máximo 3 minutos no qual você deve simular a apresentação da 
sua análise para o diretor;

### Observações
- As visualizações, queries e código Python que sustentam a análise devem estar no arquivo .pdf do desafio;
- Utilize apenas Python e SQL para resolução;
- Não é necessário a construção de aplicação com streamlit, flask ou similar;

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
