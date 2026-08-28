# Desafio Técnico: Analista de Dados e BI (Python/SQL)

Olá! Meu nome é **Rafaela Ayres** e este repositório contém a minha resolução para o desafio técnico do processo seletivo para a vaga de **Analista de Dados e BI (Python/SQL - Remoto)**.

O desafio é composto por duas frentes principais:

- **3 Testes de consultas em SQL**
- **3 Cases práticos desenvolvidos em Python**

---

## 🚀 Como Executar o Projeto

Para garantir a reprodutibilidade dos scripts, certifique-se de ter o **Python 3** instalado em sua máquina e siga os passos abaixo no seu terminal:

### 1. Clonar o repositório e acessar a pasta do projeto

```bash
cd desafio_RafaelaAyres
```

### 2. Configurar o Ambiente Virtual (venv)

Crie e ative o ambiente isolado para evitar conflitos de dependências:

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Prompt de Comando / PowerShell):**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar as Dependências

Com o ambiente virtual ativo, instale os pacotes necessários listados dentro da pasta:

```bash
pip install -r requirements.txt
```

> **Nota:** Certifique-se de que o arquivo de requerimentos está nesta pasta antes de rodar o comando.

---

## ⚙️ Estrutura do Projeto e Conexão

### Conexão com o Banco de Dados

Toda a lógica de autenticação e comunicação com o banco de dados está centralizada na pasta de módulos principais:

- 📂 `src/conexao_db.py`

---

## 📊 Resolução dos Testes

### 1. Testes SQL

Os arquivos de consulta estruturada contendo a lógica individual de cada questão estão localizados em:

- 📂 `sql/questao_1.sql`
- 📂 `sql/questao_2.sql`
- 📂 `sql/questao_3.sql`

Para visualizar as saídas e resultados reais dessas consultas no terminal, execute o script unificado de respostas:

```bash
python src/respostas_questoes.py
```

### 2. Cases Python

Os scripts de manipulação de dados, lógica de negócios e análises gráficas estão separados por arquivos dentro do diretório de cases:

- 📂 `src/cases/questao_1.py`
- 📂 `src/cases/questao_2.py`
- 📂 `src/cases/questao_3.py`

**Como executar:** Você pode rodar cada arquivo separadamente para analisar os outputs. Exemplo:

```bash
python src/cases/questao_1.py
```

> 📌 **Observação sobre a Questão 3:** Os gráficos e visualizações gerados por este script serão salvos automaticamente no diretório de saída em `src/output/`.

---

Disponível para feedbacks e dúvidas técnicas sobre a arquitetura da solução!