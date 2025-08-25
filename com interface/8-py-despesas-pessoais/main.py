import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
from user_operations import UserOperations
import os
import sys
from database import Database


# Função para lidar com caminhos de recursos em diferentes ambientes (desenvolvimento e executável)
def resource_path(relative_path):
    try:
        # Tenta obter o caminho base do executável criado pelo PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver em um executável, usa o diretório atual
        base_path = os.path.abspath(".")

    # Retorna o caminho absoluto combinando o caminho base e o relativo
    return os.path.join(base_path, relative_path)


def get_db_path():
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável
        application_path = os.path.dirname(sys.executable)
    else:
        # Se estiver rodando em desenvolvimento
        application_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(application_path, 'cadastro_simplificado.db')


# Classe principal da interface gráfica
class TelaCadastro(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Usa o novo método para obter o caminho do banco de dados
        db_path = get_db_path()
        self.db = Database(db_path)
        self.user_operations = UserOperations(self.db, self)
        self.setup_ui()
        self.selected_user = None
        self.set_icon()

    # Define o ícone da janela principal
    def set_icon(self):
        icon_path = resource_path("assets/inicio.ico")
        try:
            self.iconbitmap(icon_path)
        except:
            print(f"Não foi possível carregar o ícone: {icon_path}")

    # Configuração dos elementos da interface do usuário
    def setup_ui(self):
        self.title("Cadastro e Lista de Usuários")
        self.geometry("600x500")

        # Carrega as imagens para os modos claro e escuro
        self.light_image = ctk.CTkImage(Image.open(resource_path("assets/light_icon.png")), size=(20, 20))
        self.dark_image = ctk.CTkImage(Image.open(resource_path("assets/dark_icon.png")), size=(20, 20))

        # Tenta carregar o ícone padrão
        try:
            icon_image = Image.open(resource_path("assets/inicio.png"))
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.iconphoto(False, icon_photo)
        except Exception as e:
            print(f"Não foi possível carregar o ícone padrão: {e}")

        # Frame principal
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Frame superior para o título e botão de modo
        self.top_frame = ctk.CTkFrame(self.frame)
        self.top_frame.pack(fill="x", padx=10, pady=5)

        # Título
        self.label = ctk.CTkLabel(self.top_frame, text="Cadastro de Usuários", font=("Roboto", 24))
        self.label.pack(side="left", pady=10)

        # Botão de troca de modo (claro/escuro)
        self.switch_mode_btn = ctk.CTkButton(self.top_frame, text="", width=40, height=40,
                                            command=self.toggle_mode, image=self.dark_image)
        self.switch_mode_btn.pack(side="right", padx=10)

        # Campo de entrada para o nome
        self.nome_entry = ctk.CTkEntry(self.frame, placeholder_text="Ex:Salário, Compras")
        self.nome_entry.pack(pady=5, padx=10)

        self.nome_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome")
        self.nome_entry.pack(pady=5, padx=10)

        # Frame para os botões
        self.button_frame = ctk.CTkFrame(self.frame)
        self.button_frame.pack(pady=5)

        # Botões de ação
        self.cadastrar_btn = ctk.CTkButton(self.button_frame, text="Cadastrar", fg_color="green", hover_color="darkgreen", command=self.user_operations.cadastrar)
        self.cadastrar_btn.pack(side="left", padx=5)

        self.atualizar_btn = ctk.CTkButton(self.button_frame, text="Atualizar", fg_color="blue", hover_color="darkblue", command=self.user_operations.atualizar_usuario)
        self.atualizar_btn.pack(side="left", padx=5)

        self.excluir_btn = ctk.CTkButton(self.button_frame, text="Excluir", fg_color="red", hover_color="darkred", command=self.user_operations.excluir_usuario)
        self.excluir_btn.pack(side="left", padx=5)

        # Configuração do estilo da Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Roboto", 10, "bold"))

        # Treeview para exibir os usuários
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nome"), show="headings")
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Nome", text="Nome", anchor="center")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome", width=400, anchor="center")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Vincula a seleção na Treeview a um método
        self.tree.bind("<<TreeviewSelect>>", self.on_user_select)

        # Carrega os dados iniciais
        self.carregar_dados()

    # Carrega os dados dos usuários na Treeview
    def carregar_dados(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_all_users():
            self.tree.insert("", "end", values=row)

    # Manipula o evento de seleção de um usuário na Treeview
    def on_user_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            self.selected_user = self.tree.item(item, "values")
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, self.selected_user[1])

    # Alterna entre os modos claro e escuro
    def toggle_mode(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.switch_mode_btn.configure(image=self.light_image)
        else:
            ctk.set_appearance_mode("Dark")
            self.switch_mode_btn.configure(image=self.dark_image)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = TelaCadastro()
    app.mainloop()
