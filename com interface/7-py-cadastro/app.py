import customtkinter as ctk
import sqlite3
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os


# Classe para gerenciar a conexão com o banco de dados SQLite
class Database:
    def __init__(self, db_name='cadastro.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.create_admin_user()  # Novo método para criar usuário admin

    # Cria as tabelas de usuários e credenciais se elas não existirem
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        ''')
        # Nova tabela para armazenar as credenciais de login
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS credenciais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    # Novo método para criar o usuário admin se não existir
    def create_admin_user(self):
        self.cursor.execute("SELECT * FROM credenciais WHERE nome_usuario = 'admin'")
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO credenciais (nome_usuario, senha) VALUES (?, ?)", ('admin', 'admin'))
            self.conn.commit()
            print("Usuário admin criado com sucesso.")

    # Novo método para verificar as credenciais de login
    def verificar_credenciais(self, nome_usuario, senha):
        self.cursor.execute("SELECT * FROM credenciais WHERE nome_usuario = ? AND senha = ?", (nome_usuario, senha))
        return self.cursor.fetchone() is not None

    # Insere um novo usuário no banco de dados
    def insert_user(self, nome, email, telefone):
        self.cursor.execute("INSERT INTO usuarios (nome, email, telefone) VALUES (?, ?, ?)", (nome, email, telefone))
        self.conn.commit()

    # Retorna todos os usuários do banco de dados
    def get_all_users(self):
        self.cursor.execute("SELECT * FROM usuarios")
        return self.cursor.fetchall()

    # Atualiza os dados de um usuário existente
    def update_user(self, id, nome, email, telefone):
        self.cursor.execute("UPDATE usuarios SET nome=?, email=?, telefone=? WHERE id=?", (nome, email, telefone, id))
        self.conn.commit()

    # Remove um usuário do banco de dados
    def delete_user(self, id):
        self.cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))
        self.conn.commit()

    # Fecha a conexão com o banco de dados
    def close(self):
        self.conn.close()


# Nova classe para a tela de login
class TelaLogin(ctk.CTk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setup_ui()

    # Configura a interface do usuário para a tela de login
    def setup_ui(self):
        self.title("Login")
        self.geometry("300x250")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "entrada.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Login", font=("Roboto", 24))
        self.label.pack(pady=10)

        self.nome_usuario_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome de Usuário")
        self.nome_usuario_entry.pack(pady=5, padx=10, fill="x")

        self.senha_entry = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*")
        self.senha_entry.pack(pady=5, padx=10, fill="x")

        self.login_btn = ctk.CTkButton(self.frame, text="Entrar", command=self.fazer_login)
        self.login_btn.pack(pady=10)

    # Método para verificar as credenciais e fazer login
    def fazer_login(self):
        nome_usuario = self.nome_usuario_entry.get()
        senha = self.senha_entry.get()

        if self.db.verificar_credenciais(nome_usuario, senha):
            self.destroy()  # Fecha a tela de login
            app = TelaCadastro(self.db)  # Abre a tela principal
            app.mainloop()
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha inválidos.")


# Classe principal para a tela de cadastro
class TelaCadastro(ctk.CTk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setup_ui()

    # Configura a interface do usuário
    def setup_ui(self):
        self.title("Cadastro de Usuários")
        self.geometry("400x400")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "entrada.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # Frame principal
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Carrega ícones para o botão de tema
        self.light_icon = ctk.CTkImage(Image.open(os.path.join(script_dir, "light_icon.png")), size=(20, 20))
        self.dark_icon = ctk.CTkImage(Image.open(os.path.join(script_dir, "dark_icon.png")), size=(20, 20))

        # Botão para alternar o tema
        self.tema_btn = ctk.CTkButton(self.frame, image=self.dark_icon, text="", width=30, height=30,
                                      command=self.alternar_tema)
        self.tema_btn.place(relx=0.95, rely=0.05, anchor="ne")

        # Elementos da interface
        self.label = ctk.CTkLabel(self.frame, text="Cadastro de Usuários", font=("Roboto", 24))
        self.label.pack(pady=10)

        self.nome_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome")
        self.nome_entry.pack(pady=5, padx=10, fill="x")

        self.email_entry = ctk.CTkEntry(self.frame, placeholder_text="E-mail")
        self.email_entry.pack(pady=5, padx=10, fill="x")

        self.telefone_entry = ctk.CTkEntry(self.frame, placeholder_text="Telefone")
        self.telefone_entry.pack(pady=5, padx=10, fill="x")
        self.telefone_entry.bind("<KeyRelease>", self.formatar_telefone)

        # Frame para os botões
        self.btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        # Carrega ícones para os botões
        self.cadastrar_icon = ctk.CTkImage(Image.open(os.path.join(script_dir, "cadastrar_icon.png")), size=(20, 20))
        self.cancelar_icon = ctk.CTkImage(Image.open(os.path.join(script_dir, "cancelar_icon.png")), size=(20, 20))
        self.listar_icon = ctk.CTkImage(Image.open(os.path.join(script_dir, "listar_icon.png")), size=(20, 20))

        # Botões
        self.cadastrar_btn = ctk.CTkButton(self.btn_frame, text="Cadastrar", image=self.cadastrar_icon,
                                           compound="left", fg_color="green", hover_color="darkgreen",
                                           command=self.cadastrar)
        self.cadastrar_btn.pack(side="left", padx=5)

        self.cancelar_btn = ctk.CTkButton(self.btn_frame, text="Cancelar", image=self.cancelar_icon,
                                          compound="left", fg_color="darkred", hover_color="red",
                                          command=self.quit)
        self.cancelar_btn.pack(side="left", padx=5)

        self.listar_btn = ctk.CTkButton(self.frame, text="Listar Cadastros", image=self.listar_icon,
                                        compound="left", command=self.abrir_lista)
        self.listar_btn.pack(pady=10, padx=10, fill="x")

    # Formata o número de telefone enquanto o usuário digita
    def formatar_telefone(self, event):
        telefone = self.telefone_entry.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")[:11]
        formatado = ""

        if len(telefone) > 0:
            formatado += f"({telefone[:2]})"
            if len(telefone) > 2:
                formatado += f" {telefone[2:7]}"
                if len(telefone) > 7:
                    formatado += f"-{telefone[7:]}"

        self.telefone_entry.delete(0, 'end')
        self.telefone_entry.insert(0, formatado)

    # Cadastra um novo usuário
    def cadastrar(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()

        if nome and email and telefone:
            self.db.insert_user(nome, email, telefone)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    # Limpa os campos após o cadastro
    def limpar_campos(self):
        self.nome_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.telefone_entry.delete(0, 'end')

    # Abre a janela de listagem de usuários
    def abrir_lista(self):
        self.withdraw()
        lista_window = TelaLista(self, self.db)
        lista_window.grab_set()

    # Alterna entre os temas claro e escuro
    def alternar_tema(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.tema_btn.configure(image=self.light_icon)
        else:
            ctk.set_appearance_mode("Dark")
            self.tema_btn.configure(image=self.dark_icon)


# Classe para a tela de listagem de usuários
class TelaLista(ctk.CTkToplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.setup_ui()
        self.carregar_dados()

    # Configura a interface da tela de listagem
    def setup_ui(self):
        self.title("Lista de Usuários")
        self.geometry("680x400")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "entrada.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Lista de Usuários", font=("Roboto", 28))
        self.label.pack(pady=12, padx=10)

        # Configura o estilo da Treeview
        self.style = ttk.Style()
        self.configurar_estilo_treeview()

        # Cria a Treeview para exibir os usuários
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nome", "E-mail", "Telefone"), show="headings",
                                 style="Treeview")
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Nome", text="Nome", anchor="center")
        self.tree.heading("E-mail", text="E-mail", anchor="center")
        self.tree.heading("Telefone", text="Telefone", anchor="center")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome", width=180, anchor="center")
        self.tree.column("E-mail", width=220, anchor="center")
        self.tree.column("Telefone", width=150, anchor="center")

        self.tree.pack(pady=12, padx=10, fill="both", expand=True)

        # Frame para os botões
        self.btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.btn_frame.pack(pady=12, padx=10)

        # Carrega ícones para os botões
        self.atualizar_icon = ctk.CTkImage(Image.open(os.path.join(script_dir, "atualizar_icon.png")), size=(20, 20))
        self.excluir_icon = ctk.CTkImage(Image.open(os.path.join(script_dir, "excluir_icon.png")), size=(20, 20))
        self.voltar_icon = ctk.CTkImage(Image.open(os.path.join(script_dir, "voltar_icon.png")), size=(20, 20))

        # Botões
        self.atualizar_btn = ctk.CTkButton(self.btn_frame, text="Atualizar", image=self.atualizar_icon,
                                           compound="left", fg_color="green", hover_color="darkgreen",
                                           command=self.atualizar_usuario)
        self.atualizar_btn.pack(side="left", padx=5)

        self.excluir_btn = ctk.CTkButton(self.btn_frame, text="Excluir", image=self.excluir_icon,
                                         compound="left", fg_color="darkred", hover_color="red",
                                         command=self.excluir_usuario)
        self.excluir_btn.pack(side="left", padx=5)

        self.voltar_btn = ctk.CTkButton(self.btn_frame, text="Voltar", image=self.voltar_icon,
                                        compound="left", command=self.voltar)
        self.voltar_btn.pack(side="left", padx=5)

    # Configura o estilo da Treeview de acordo com o tema
    def configurar_estilo_treeview(self):
        modo = ctk.get_appearance_mode()
        if modo == "Dark":
            self.style.theme_use("clam")
            self.style.configure("Treeview",
                                 background="#2a2d2e",
                                 foreground="white",
                                 fieldbackground="#2a2d2e",
                                 font=("Roboto", 12))
            self.style.configure("Treeview.Heading",
                                 background="#565b5e",
                                 foreground="white",
                                 font=("Roboto", 14))
            self.style.map("Treeview", background=[('selected', '#22559b')])
            self.style.map("Treeview", foreground=[('selected', 'white')])
        else:
            self.style.theme_use("default")
            self.style.configure("Treeview",
                                 background="white",
                                 foreground="black",
                                 fieldbackground="white",
                                 font=("Roboto", 12))
            self.style.configure("Treeview.Heading",
                                 background="#e1e1e1",
                                 foreground="black",
                                 font=("Roboto", 14))
            self.style.map("Treeview", background=[('selected', '#22559b')])
            self.style.map("Treeview", foreground=[('selected', 'white')])

        self.style.configure("Treeview.Heading", relief="flat")
        self.style.map("Treeview.Heading", background=[('active', '#3484F0')])

    # Carrega os dados dos usuários na Treeview
    def carregar_dados(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_all_users():
            self.tree.insert("", "end", values=row)

    # Abre a janela para atualizar um usuário
    def atualizar_usuario(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Por favor, selecione um usuário para atualizar.")
            return

        usuario = self.tree.item(selected[0])['values']

        update_window = ctk.CTkToplevel(self)
        update_window.title("Atualizar Usuário")
        update_window.geometry("300x250")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "entrada.ico")
        if os.path.exists(icon_path):
            update_window.iconbitmap(icon_path)

        ctk.CTkLabel(update_window, text="Nome:").pack()
        nome_entry = ctk.CTkEntry(update_window)
        nome_entry.insert(0, usuario[1])
        nome_entry.pack()

        ctk.CTkLabel(update_window, text="E-mail:").pack()
        email_entry = ctk.CTkEntry(update_window)
        email_entry.insert(0, usuario[2])
        email_entry.pack()

        ctk.CTkLabel(update_window, text="Telefone:").pack()
        telefone_entry = ctk.CTkEntry(update_window)
        telefone_entry.insert(0, usuario[3])
        telefone_entry.pack()

        # Aplica a formatação do telefone na janela de atualização
        telefone_entry.bind("<KeyRelease>", lambda event: self.formatar_telefone_update(event, telefone_entry))

        # Função para salvar as atualizações do usuário
        def salvar_atualizacao():
            novo_nome = nome_entry.get()
            novo_email = email_entry.get()
            novo_telefone = telefone_entry.get()

            self.db.update_user(usuario[0], novo_nome, novo_email, novo_telefone)
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            update_window.destroy()
            self.carregar_dados()

        ctk.CTkButton(update_window, text="Salvar", command=salvar_atualizacao).pack(pady=10)

    # Formata o telefone na janela de atualização
    def formatar_telefone_update(self, event, entry):
        telefone = entry.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")[:11]
        formatado = ""

        if len(telefone) > 0:
            formatado += f"({telefone[:2]})"
            if len(telefone) > 2:
                formatado += f" {telefone[2:7]}"
                if len(telefone) > 7:
                    formatado += f"-{telefone[7:]}"

        entry.delete(0, 'end')
        entry.insert(0, formatado)

    # Exclui o usuário selecionado
    def excluir_usuario(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Por favor, selecione um usuário para excluir.")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este usuário?"):
            usuario = self.tree.item(selected[0])['values']
            self.db.delete_user(usuario)
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
            self.destroy_dados()

    # Volta para a tela principal
    def voltar(self):
        self.master.deiconify()
        self.destroy()


# Classe principal do aplicativo
class App:
    def __init__(self):
        ctk.set_appearance_mode("dark")   # Define o tema inicial como escuro
        ctk.set_default_color_theme("blue")  # Define o tema de cores como azul
        self.db = Database()  # Inicializa a conexão com o banco de dados
        self.login_window = TelaLogin(self.db)  # Cria a janela de login

    # Inicia a execução do aplicativo
    def run(self):
        self.login_window.mainloop()

    # Fecha a conexão com o banco de dados quando o aplicativo é encerrado
    def __del__(self):
        self.db.close()


# Ponto de entrada do programa
if __name__ == "__main__":
    app = App()
    app.run()