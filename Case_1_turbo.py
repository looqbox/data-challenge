'''
[continuação]

5 - criar uma interface amigável que a pessoa possa selecionar entre listas suspensas para selecionar intervalo de consulta, codigo de produto e store code
Interface realizada com auxílio de IA - Calude Code.
Utilizando tkinter, pois a solicitação foi executar apenas com python.
Premissas:
- Lista suspensa com DISTINCT das colunas, para selecionar apenas entre itens existentes.
- Calendário completo para selecionar o intervalo (sem limite)
- Tela abaixo para apresentar o resultado em formato friendly para usuários de outras áreas.

'''

#Parte 3


import calendar
import os
from datetime import datetime

import pymysql
import tkinter as tk
from tkinter import messagebox, ttk
from dotenv import load_dotenv

load_dotenv()


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


def carregar_distintos(coluna, tabela):
    """Retorna os valores distintos de uma coluna da tabela informada, em ordem crescente."""
    sql = f"SELECT DISTINCT {coluna} FROM {tabela}"
    conexao = get_connection()
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            linhas = cursor.fetchall()
    finally:
        conexao.close()
    valores = [linha[coluna] for linha in linhas if linha[coluna] is not None]
    try:
        valores.sort(key=lambda v: int(v))
    except (ValueError, TypeError):
        valores.sort()
    return valores


def retrieve_data(product_code, store_code, date):
    """Consulta as vendas filtrando por produto, loja e intervalo de datas."""
    data_inicio = date[0]
    data_fim = date[1]
    conexao = get_connection()
    try:
        with conexao.cursor() as cursor:
            sql = """
            SELECT * FROM data_product_sales dps
            WHERE dps.PRODUCT_CODE = %s
            AND dps.STORE_CODE = %s
            AND dps.`DATE` BETWEEN %s AND %s
            """
            cursor.execute(sql, (product_code, store_code, data_inicio, data_fim))
            resultados = cursor.fetchall()
    finally:
        conexao.close()
    return resultados


class SeletorData(tk.Toplevel):
    """Calendario simples feito 100% com tkinter para escolher uma data."""

    MESES = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro',
    ]
    DIAS_SEMANA = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']

    def __init__(self, master, callback, data_inicial=None):
        super().__init__(master)
        self.callback = callback
        self.title('Selecionar data')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        base = data_inicial or datetime.today()
        self.ano = base.year
        self.mes = base.month

        cabecalho = ttk.Frame(self, padding=(8, 8, 8, 4))
        cabecalho.pack(fill='x')

        ttk.Button(cabecalho, text='<', width=3, command=self.mes_anterior).pack(side='left')
        self.label_mes = ttk.Label(cabecalho, anchor='center', font=('Segoe UI', 10, 'bold'))
        self.label_mes.pack(side='left', expand=True, fill='x')
        ttk.Button(cabecalho, text='>', width=3, command=self.proximo_mes).pack(side='left')

        self.grade = ttk.Frame(self, padding=(8, 0, 8, 8))
        self.grade.pack()

        self._desenhar_calendario()

    def mes_anterior(self):
        self.mes -= 1
        if self.mes < 1:
            self.mes = 12
            self.ano -= 1
        self._desenhar_calendario()

    def proximo_mes(self):
        self.mes += 1
        if self.mes > 12:
            self.mes = 1
            self.ano += 1
        self._desenhar_calendario()

    def _desenhar_calendario(self):
        for widget in self.grade.winfo_children():
            widget.destroy()

        self.label_mes.config(text=f'{self.MESES[self.mes - 1]} {self.ano}')

        for col, nome in enumerate(self.DIAS_SEMANA):
            ttk.Label(self.grade, text=nome, anchor='center', width=4,
                      font=('Segoe UI', 9, 'bold')).grid(row=0, column=col, padx=1, pady=1)

        semanas = calendar.monthcalendar(self.ano, self.mes)
        for r, semana in enumerate(semanas, start=1):
            for c, dia in enumerate(semana):
                if dia == 0:
                    continue
                tk.Button(
                    self.grade, text=str(dia), width=4, relief='flat',
                    command=lambda d=dia: self._selecionar(d),
                ).grid(row=r, column=c, padx=1, pady=1)

    def _selecionar(self, dia):
        data = datetime(self.ano, self.mes, dia)
        self.callback(data.strftime('%d-%m-%Y'))
        self.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Consulta de Vendas')
        self.geometry('900x600')
        self.minsize(700, 500)

        self._montar_filtros()
        self._montar_tabela()
        self._carregar_listas()

    def _montar_filtros(self):
        filtros = ttk.LabelFrame(self, text='Filtros', padding=10)
        filtros.pack(fill='x', padx=10, pady=10)

        ttk.Label(filtros, text='Código do produto:').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.combo_produto = ttk.Combobox(filtros, state='readonly', width=20)
        self.combo_produto.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        ttk.Label(filtros, text='Código da loja:').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.combo_loja = ttk.Combobox(filtros, state='readonly', width=20)
        self.combo_loja.grid(row=0, column=3, sticky='w', padx=5, pady=5)

        ttk.Label(filtros, text='Data início (DD-MM-AAAA):').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.entry_inicio = ttk.Entry(filtros, width=18)
        self.entry_inicio.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        ttk.Button(filtros, text='Selecionar',
                   command=lambda: self._abrir_calendario(self.entry_inicio)).grid(row=1, column=1, sticky='e', padx=5)

        ttk.Label(filtros, text='Data fim (DD-MM-AAAA):').grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.entry_fim = ttk.Entry(filtros, width=18)
        self.entry_fim.grid(row=1, column=3, sticky='w', padx=5, pady=5)
        ttk.Button(filtros, text='Selecionar',
                   command=lambda: self._abrir_calendario(self.entry_fim)).grid(row=1, column=3, sticky='e', padx=5)

        ttk.Button(filtros, text='Consultar', command=self._consultar).grid(
            row=2, column=0, columnspan=4, pady=(10, 0))

        self.label_status = ttk.Label(filtros, text='')
        self.label_status.grid(row=3, column=0, columnspan=4, sticky='w', pady=(5, 0))

    def _montar_tabela(self):
        container = ttk.LabelFrame(self, text='Resultado', padding=10)
        container.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(container, show='headings')
        scroll_y = ttk.Scrollbar(container, orient='vertical', command=self.tree.yview)
        scroll_x = ttk.Scrollbar(container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scroll_y.grid(row=0, column=1, sticky='ns')
        scroll_x.grid(row=1, column=0, sticky='ew')
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

    def _carregar_listas(self):
        try:
            produtos = carregar_distintos('PRODUCT_COD', 'data_product')
            lojas = carregar_distintos('STORE_CODE', 'data_store_cad')
        except Exception as erro:
            messagebox.showerror('Erro de conexão',
                                 f'Não foi possível carregar os dados do banco:\n{erro}')
            return
        self.combo_produto['values'] = produtos
        self.combo_loja['values'] = lojas

    def _abrir_calendario(self, entry):
        valor_atual = entry.get()
        data_inicial = None
        if valor_atual:
            try:
                data_inicial = datetime.strptime(valor_atual, '%d-%m-%Y')
            except ValueError:
                data_inicial = None

        def aplicar(data_str):
            entry.delete(0, 'end')
            entry.insert(0, data_str)

        SeletorData(self, aplicar, data_inicial)

    def _consultar(self):
        produto = self.combo_produto.get()
        loja = self.combo_loja.get()
        data_ini_raw = self.entry_inicio.get()
        data_fim_raw = self.entry_fim.get()

        if not produto or not loja or not data_ini_raw or not data_fim_raw:
            messagebox.showwarning('Campos obrigatórios',
                                   'Selecione produto, loja, data de início e data de fim.')
            return

        try:
            data_inicio = datetime.strptime(data_ini_raw, '%d-%m-%Y').strftime('%Y-%m-%d')
            data_fim = datetime.strptime(data_fim_raw, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showwarning('Data inválida',
                                   'Use o formato DD-MM-AAAA nas datas (ex.: 31-12-2019).')
            return

        if data_inicio > data_fim:
            messagebox.showwarning('Datas inválidas',
                                   'A data de início não pode ser maior que a data de fim.')
            return

        try:
            resultados = retrieve_data(produto, loja, [data_inicio, data_fim])
        except Exception as erro:
            messagebox.showerror('Erro na consulta', f'Falha ao consultar o banco:\n{erro}')
            return

        self._preencher_tabela(resultados)

    def _preencher_tabela(self, resultados):
        self.tree.delete(*self.tree.get_children())

        if not resultados:
            self.tree['columns'] = ()
            self.label_status.config(text='Nenhum registro encontrado.')
            messagebox.showinfo('Sem resultados', 'Nenhum registro encontrado para os filtros selecionados.')
            return

        colunas = list(resultados[0].keys())
        self.tree['columns'] = colunas
        for coluna in colunas:
            self.tree.heading(coluna, text=coluna)
            self.tree.column(coluna, width=120, anchor='center')

        for linha in resultados:
            self.tree.insert('', 'end', values=[linha[c] for c in colunas])

        self.label_status.config(text=f'{len(resultados)} registro(s) encontrado(s).')


if __name__ == '__main__':
    App().mainloop()
