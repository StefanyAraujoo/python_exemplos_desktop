import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
from user_operations import UserOperations
import os
import sys

# Função para lidar com caminhos de recursos (mesma do main.py)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TelaCadastro(ctk.CTk):
    def __init__(self, db):
        super().__init__()  # Inicializa a classe pai (CTk)
        self.db = db  # Armazena a instância do banco de dados
        self.user_operations = UserOperations(db, self)  # Cria instância de operações de usuário
        self.setup_ui()  # Configura a interface do usuário
        self.selected_user = None  # Armazena o usuário selecionado na lista
        self.set_icon()  # Define o ícone da janela

    def set_icon(self):
        # Define o ícone da janela
        icon_path = resource_path("assets/inicio.ico")
        try:
            self.iconbitmap(icon_path)
        except:
            print(f"Não foi possível carregar o ícone: {icon_path}")

    def setup_ui(self):
        # Configura a interface do usuário
        self.title("Cadastro e Lista de Usuários")
        self.geometry("600x500")

        # Tenta carregar o ícone padrão
        try:
            icon_image = Image.open(resource_path("assets/inicio.png"))
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.iconphoto(False, icon_photo)
        except Exception as e:
            print(f"Não foi possível carregar o ícone padrão: {e}")

        # Cria o frame principal
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Adiciona o título
        self.label = ctk.CTkLabel(self.frame, text="Cadastro de Usuários", font=("Roboto", 24))
        self.label.pack(pady=10)

        # Cria o campo de entrada para o nome
        self.nome_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome")
        self.nome_entry.pack(pady=5, padx=10, fill="x")

        # Cria o frame para os botões
        self.button_frame = ctk.CTkFrame(self.frame)
        self.button_frame.pack(pady=5)

        # Adiciona os botões de ação
        self.cadastrar_btn = ctk.CTkButton(self.button_frame, text="Cadastrar",
        fg_color="green", hover_color="darkgreen",
        command=self.user_operations.cadastrar)
        self.cadastrar_btn.pack(side="left", padx=5)

        self.atualizar_btn = ctk.CTkButton(self.button_frame, text="Atualizar",
        fg_color="blue", hover_color="darkblue",
        command=self.user_operations.atualizar_usuario)
        self.atualizar_btn.pack(side="left", padx=5)

        self.excluir_btn = ctk.CTkButton(self.button_frame, text="Excluir",
        fg_color="red", hover_color="darkred",
        command=self.user_operations.excluir_usuario)
        self.excluir_btn.pack(side="left", padx=5)

        # Configura o estilo da Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Roboto', 10, 'bold'))

        # Cria a Treeview para exibir os usuários
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nome"), show="headings")
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Nome", text="Nome", anchor="center")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome", width=400, anchor="center")
        self.tree.pack(pady=12, padx=10, fill="both", expand=True)

        # Associa a seleção na Treeview ao método on_user_select
        self.tree.bind("<<TreeviewSelect>>", self.on_user_select)

        # Carrega os dados iniciais
        self.carregar_dados()

    def carregar_dados(self):
        # Limpa todos os itens existentes na Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Insere todos os usuários do banco de dados na Treeview
        for row in self.db.get_all_users():
            self.tree.insert("", "end", values=row)

    def on_user_select(self, event):
        # Manipula o evento de seleção de um usuário na Treeview
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            self.selected_user = self.tree.item(item, "values")
            self.nome_entry.delete(0, 'end')
            self.nome_entry.insert(0, self.selected_user[1])