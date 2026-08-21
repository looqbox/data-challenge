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

## Questão 1: SQL - Performance por Regional

A diretoria comercial acompanha a performance das regionais contra a meta do
mês. Você precisa entregar a consulta que alimenta esse acompanhamento.

Escreva **uma query** que retorne, por **regional**, referente a **julho de
2026**:

1. Faturamento líquido;
2. Ticket médio;
3. Peças por atendimento (PA);
4. Atingimento de meta;
5. Variação de faturamento contra julho de 2025, considerando apenas as lojas com faturamento em ambos períodos.

Ordene do maior gap absoluto contra a meta para o menor.

### Fonte

| Tabela       | Conteúdo                       |
| ------------ | ------------------------------ |
| `dim_loja`   | Cadastro de lojas              |
| `fato_venda` | Movimento de venda, nível item |
| `fato_meta`  | Meta por filial                |

### Entrega

- A query desenvolvida.
- O resultado, com todas as regionais.
- Um parágrafo curto com as premissas adotadas.

---
## Questão 2: Reconstrução de estoque

### A) Saldo diário

O time de suprimentos precisa saber **qual o saldo (diferença entre entradas e saídas) de estoque de cada SKU em
cada loja, dia a dia**. O sistema de origem grava apenas as movimentações, e não
o saldo. Cabe a você reconstruir a curva diária a partir do histórico de
movimentos.

Construa o saldo **diário** por loja e SKU na janela de **2026-04-01 a
2026-07-31**, e valide o resultado. 

| Tabela | Conteúdo |
|---|---|
| `movimentacoes` | Movimentações de produtos |

- Salve o resultado em um arquivo CSV: chamado `saldo_diario.csv`;

### B) Reconstrua o estoque
Após alguns dias da sua entrega, o estagiário da área encontrou um arquivo
`estoque_20260731.csv` com o estoque por loja e SKU do dia 2026-07-31. 
A partir desse csv e do arquivo `saldo_diario.csv` que você elaborou no item anterior,
você deve reconstruir o estoque diário do período de 2026-04-01 a 2026-07-31.

- Utilize apenas Python para essa tarefa;
- Para este item, você não deve consultar a base de dados;
- O retorno deve ser um arquivo csv chamado: `estoque_diario.csv`;
- Se houver inconsistências, aponte.

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

### Entrega

- Monte um conjunto de visualizações (gráficos, tabelas, etc.) que auxiliem o diretor
entender as causas dessa queda no indicador, mostrando para ele os principais 
ofensores e demais informações relevantes para a análise;
- Grave um vídeo de no máximo 3 minutos no qual você deve simular a apresentação da 
sua análise para o diretor;

### Observações
- As visualizações, queries e código Python que sustentam a análise devem estar no
arquivo .pdf do desafio;
- Utilize apenas Python e SQL para resolução;
- Não é necessário a construção de aplicação com streamlit, flask ou similar;
- Não é permitido a utilização de ferramentas como PowerBI, Tableau, Looker Studio e similares.

---

## Como entregar

Arquivo .zip contendo:
- Arquivo **PDF único** com TODOS os códigos, visualizações e explicações em cada questão. A organização e clareza também serão avaliadas;
- Arquivos .csv gerados nos itens 2A e 2B;
- Vídeo em formato mp4;
- (Opcional) Arquivos .py ou ipynb e .sql usados nas questões - Lembrando que todos os códigos devem estar obrigatoriamente no arquivo PDF.
  
**Não abra pull request e não faça fork deste repositório.**

---

## Orientações

- Sempre que o enunciado for ambíguo, decida e registre a premissa. Premissa
  declarada vale ponto. Premissa escondida no código custa ponto.
- Preferimos uma entrega menor e validada a uma entrega completa e não
  conferida. Se faltar tempo, corte escopo e diga o que cortou.
- Se algo travar no acesso ao banco, responda o e-mail do convite. Tempo perdido
  em configuração de ambiente não conta contra você.
- IMPORTANTE: O candidato deve apontar claramente onde utilizou o auxílio de ferramentas de LLM. Sobe pena de perda de pontos em caso de omissão.

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

## Links úteis

- [Documentação do pandas](https://pandas.pydata.org/docs/)
- [Data Visualization Catalogue](https://datavizcatalogue.com/)
- [Guia de estilo PEP 8](https://peps.python.org/pep-0008/)
