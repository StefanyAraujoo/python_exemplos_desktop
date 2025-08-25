import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import locale

# Configura locale para formatação monetária
locale.setlocale(locale.LC_ALL, '')

DB_NAME = "financeiro.db"

# Banco de dados
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_transacao(tipo, descricao, valor, data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO transacoes (tipo, descricao, valor, data) VALUES (?, ?, ?, ?)',
              (tipo, descricao, valor, data))
    conn.commit()
    conn.close()

def deletar_transacao(id_):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM transacoes WHERE id=?', (id_,))
    conn.commit()
    conn.close()

def obter_transacoes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, tipo, descricao, valor, data FROM transacoes ORDER BY data DESC, id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def calcular_saldo():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT tipo, valor FROM transacoes')
    saldo = 0.0
    for tipo, valor in c.fetchall():
        if tipo == 'Receita':
            saldo += valor
        else:
            saldo -= valor
    conn.close()
    return saldo

# Interface gráfica
class FinanceiroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Controle Financeiro Pessoal")
        self.geometry("650x500")
        self.resizable(False, False)
        self.configure(bg="#f5f6fa")
        self.iconbitmap(False)  # Remova ou adicione um ícone se desejar

        self.criar_widgets()
        self.atualizar_lista()
        self.atualizar_saldo()

    def criar_widgets(self):
        # Frame superior
        frame_top = tk.Frame(self, bg="#f5f6fa")
        frame_top.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_top, text="Descrição:", bg="#f5f6fa").grid(row=0, column=0, padx=5, pady=2)
        self.desc_entry = tk.Entry(frame_top, width=25)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_top, text="Valor:", bg="#f5f6fa").grid(row=0, column=2, padx=5, pady=2)
        self.valor_entry = tk.Entry(frame_top, width=12)
        self.valor_entry.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(frame_top, text="Tipo:", bg="#f5f6fa").grid(row=0, column=4, padx=5, pady=2)
        self.tipo_var = tk.StringVar(value="Despesa")
        tipo_menu = ttk.Combobox(frame_top, textvariable=self.tipo_var, values=["Receita", "Despesa"], width=10, state="readonly")
        tipo_menu.grid(row=0, column=5, padx=5, pady=2)

        tk.Button(frame_top, text="Adicionar", command=self.adicionar_transacao, bg="#44bd32", fg="white", width=12).grid(row=0, column=6, padx=5, pady=2)

        # Saldo
        self.saldo_var = tk.StringVar()
        saldo_frame = tk.Frame(self, bg="#f5f6fa")
        saldo_frame.pack(pady=5)
        tk.Label(saldo_frame, text="Saldo Atual:", font=("Arial", 12, "bold"), bg="#f5f6fa").pack(side="left")
        tk.Label(saldo_frame, textvariable=self.saldo_var, font=("Arial", 12, "bold"), bg="#f5f6fa", fg="#273c75").pack(side="left", padx=8)

        # Histórico
        historico_frame = tk.Frame(self, bg="#f5f6fa")
        historico_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("id", "data", "tipo", "descricao", "valor")
        self.tree = ttk.Treeview(historico_frame, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("data", text="Data")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("valor", text="Valor")
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("data", width=90, anchor="center")
        self.tree.column("tipo", width=70, anchor="center")
        self.tree.column("descricao", width=220)
        self.tree.column("valor", width=90, anchor="e")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(historico_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Botão deletar
        btn_frame = tk.Frame(self, bg="#f5f6fa")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Excluir Selecionado", command=self.excluir_transacao, bg="#e84118", fg="white", width=18).pack()

    def adicionar_transacao(self):
        descricao = self.desc_entry.get().strip()
        valor_str = self.valor_entry.get().replace(",", ".").strip()
        tipo = self.tipo_var.get()
        data = datetime.now().strftime("%d/%m/%Y")

        if not descricao or not valor_str:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        try:
            valor = float(valor_str)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Valor inválido", "Digite um valor numérico positivo.")
            return

        inserir_transacao(tipo, descricao, valor, data)
        self.desc_entry.delete(0, tk.END)
        self.valor_entry.delete(0, tk.END)
        self.atualizar_lista()
        self.atualizar_saldo()

    def excluir_transacao(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showinfo("Selecione", "Selecione uma transação para excluir.")
            return
        item = self.tree.item(selecionado[0])
        id_ = item['values'][0]
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta transação?"):
            deletar_transacao(id_)
            self.atualizar_lista()
            self.atualizar_saldo()

    def atualizar_lista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for id_, tipo, descricao, valor, data in obter_transacoes():
            valor_fmt = locale.currency(valor, grouping=True)
            self.tree.insert("", "end", values=(id_, data, tipo, descricao, valor_fmt))

    def atualizar_saldo(self):
        saldo = calcular_saldo()
        cor = "#44bd32" if saldo >= 0 else "#e84118"
        self.saldo_var.set(locale.currency(saldo, grouping=True))
        self.nametowidget(self.saldo_var._name).config(fg=cor)

if __name__ == "__main__":
    init_db()
    app = FinanceiroApp()
    app.mainloop()