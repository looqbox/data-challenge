'''
Case 3 - Dois graficos lado a lado em uma unica imagem

O que este script faz:
1. Conecta no banco (mesmo .env dos outros cases) e carrega a tabela IMDB_movies.
2. Trata os dados (tipos, explode de Genre) - tudo neste arquivo.
3. Monta UMA imagem com dois graficos lado a lado:
   - Esquerda : dispersao Rating medio x Receita media por ano (com linha de tendencia).
   - Direita  : area empilhada dos 6 generos mais comuns + linha de Rating medio,
                com a LEGENDA posicionada ao lado do grafico (fora da area de plotagem).
4. Salva o resultado em analise_imdb/charts/case3_graficos_lado_a_lado.png

Como rodar:
    python Case_3_graficos_lado_a_lado.py
(ou use o iniciar_Case_3.bat)
'''

import os

import numpy as np
import pandas as pd
import pymysql
import matplotlib

matplotlib.use('Agg')  # backend sem interface grafica (apenas salva arquivos)
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

load_dotenv()

sns.set_theme(style='whitegrid', palette='deep')
plt.rcParams['figure.dpi'] = 110
plt.rcParams['savefig.bbox'] = 'tight'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARTS_DIR = os.path.join(BASE_DIR, 'analise_imdb', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Conexao, carga e limpeza 
# ---------------------------------------------------------------------------
def get_connection():
    """Abre uma nova conexao com o banco usando as variaveis do .env."""
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor,
    )


def carregar_dados():
    """Le toda a tabela IMDB_movies e devolve um DataFrame."""
    conexao = get_connection()
    try:
        with conexao.cursor() as cursor:
            cursor.execute('SELECT * FROM IMDB_movies')
            linhas = cursor.fetchall()
    finally:
        conexao.close()
    return pd.DataFrame(linhas)


def limpar_dados(df):
    """Converte tipos, normaliza textos e cria a tabela explodida por genero."""
    df = df.copy()

    # Decimais e inteiros podem vir como Decimal/None -> converte para float
    for col in ['Runtime', 'Rating', 'Votes', 'RevenueMillions', 'Metascore', 'Year']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Normaliza Genre (tira espacos extras)
    df['Genre'] = df['Genre'].fillna('').str.strip()

    # Tabela "explodida" por genero: 1 linha por (filme, genero)
    df_genre = df.assign(
        Genre=df['Genre'].str.split(',')
    ).explode('Genre')
    df_genre['Genre'] = df_genre['Genre'].str.strip()
    df_genre = df_genre[df_genre['Genre'] != '']

    return df, df_genre


def preparar_series(df, df_genre):
    """Calcula o agregado por ano e o pivot dos 6 generos mais comuns."""
    por_ano = df.groupby('Year').agg(
        rating_medio=('Rating', 'mean'),
        receita_media=('RevenueMillions', 'mean'),
    )

    top_generos = df_genre['Genre'].value_counts().head(6).index
    pivot = (df_genre[df_genre['Genre'].isin(top_generos)]
             .groupby(['Year', 'Genre']).size().unstack(fill_value=0))
    pivot = pivot[top_generos]
    return por_ano, pivot


def desenhar_dispersao(ax, por_ano):
    """Dispersao rating medio x receita media (1 ponto por ano) com tendencia."""
    x = por_ano['rating_medio'].values
    y = por_ano['receita_media'].values
    r = np.corrcoef(x, y)[0, 1]

    ax.scatter(x, y, s=90, color='#4C72B0', edgecolor='white', zorder=3)
    for ano, linha in por_ano.iterrows():
        ax.annotate(int(ano),
                    (linha['rating_medio'], linha['receita_media']),
                    textcoords='offset points', xytext=(7, 4), fontsize=9)

    m, b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 100)
    ax.plot(xs, m * xs + b, '--', color='red', label=f'tendencia (r = {r:.2f})')

    ax.set_xlabel('Rating medio do ano')
    ax.set_ylabel('Receita media do ano (milhoes)')
    ax.set_title('Rating medio x Receita media por ano')
    ax.legend(loc='upper left')


def desenhar_evolucao_rating(ax1, pivot, por_ano):
    """Area empilhada dos generos + linha de rating medio, legenda fora do grafico."""
    ax1.stackplot(pivot.index, [pivot[g] for g in pivot.columns],
                  labels=list(pivot.columns), alpha=0.85)
    ax1.set_xlabel('Ano')
    ax1.set_ylabel('Numero de filmes')
    ax1.set_title('Evolucao dos 6 generos por ano + Rating medio (linha)')

    ax2 = ax1.twinx()
    ax2.plot(por_ano.index, por_ano['rating_medio'], color='black', marker='o',
             linewidth=2.5, markersize=6, label='Rating medio')
    ax2.set_ylabel('Rating medio', color='black')
    ax2.tick_params(axis='y', labelcolor='black')
    ax2.grid(False)

    # Legenda unificada posicionada ao lado do grafico (fora da area de plotagem).
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc='upper left',
               bbox_to_anchor=(1.18, 1.0), fontsize=9, borderaxespad=0.,
               frameon=True, title='Legenda')


def gerar_imagem():
    print('Carregando dados da tabela IMDB_movies...')
    df_raw = carregar_dados()
    df, df_genre = limpar_dados(df_raw)
    print(f'  {len(df)} filmes carregados.')

    por_ano, pivot = preparar_series(df, df_genre)

    # 2 graficos lado a lado; o da direita ganha mais largura por causa da legenda externa.
    fig, (ax_disp, ax_evol) = plt.subplots(
        1, 2, figsize=(20, 7), gridspec_kw={'width_ratios': [1, 1.35]})

    desenhar_dispersao(ax_disp, por_ano)
    desenhar_evolucao_rating(ax_evol, pivot, por_ano)

    fig.suptitle('Case 3 - Rating x Receita e Evolucao dos generos', fontsize=14)
    # Reserva espaco a direita para a legenda externa nao ser cortada.
    fig.subplots_adjust(right=0.82, wspace=0.25, top=0.9)

    caminho = os.path.join(CHARTS_DIR, 'case3_graficos_lado_a_lado.png')
    fig.savefig(caminho)
    plt.close(fig)
    print('\nConcluido!')
    print(f'  Imagem: {caminho}')


if __name__ == '__main__':
    gerar_imagem()
