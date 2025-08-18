import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import sys
from PIL import Image, ImageTk

def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso, funciona para dev e para o PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class FormularioInscricao:
    def __init__(self, master):
        self.master = master
        self.master.title("Formulário de Inscrição")
        self.master.geometry("500x550")

        # Configurando o ícone da janela
        self.set_icon()

        # Lista de temas disponíveis no ttkbootstrap
        # https://ttkbootstrap.readthedocs.io/en/latest/themes
        self.temas = ["darkly", "flatly", "litera", "minty", "lumen", "sandstone", "yeti", "pulse",
                      "united", "morph", "journal", "darkly", "superhero", "solar", "cyborg", "vapor"]

        # Configuração do estilo inicial
        self.style = ttk.Style("darkly")

        # Criação do frame principal
        self.frame = ttk.Frame(self.master, padding=20)
        self.frame.pack(fill=BOTH, expand=YES)

        # Título
        ttk.Label(self.frame, text="Formulário de Inscrição", font=("TkDefaultFont", 16, "bold")).pack(pady=10)

        # Campo Nome
        ttk.Label(self.frame, text="Nome").pack(anchor=W, pady=(10, 0))
        self.nome_entry = ttk.Entry(self.frame, width=50)
        self.nome_entry.pack(fill=X)

        # Campo Email
        ttk.Label(self.frame, text="Email").pack(anchor=W, pady=(10, 0))
        self.email_entry = ttk.Entry(self.frame, width=50)
        self.email_entry.pack(fill=X)

        # Campo Idade
        ttk.Label(self.frame, text="Idade").pack(anchor=W, pady=(10, 0))
        self.idade_entry = ttk.Entry(self.frame, width=50)
        self.idade_entry.pack(fill=X)

        # Frame para Checkbox e Combobox
        self.opcoes_frame = ttk.Frame(self.frame)
        self.opcoes_frame.pack(fill=X, pady=10)

        # Checkbox Lembrar dados
        self.lembrar_var = ttk.BooleanVar()
        self.lembrar_check = ttk.Checkbutton(self.opcoes_frame, text="Lembrar dados?", variable=self.lembrar_var,
                                             bootstyle="round-toggle")
        self.lembrar_check.pack(side=LEFT)

        # Combobox para seleção de temas
        self.tema_var = ttk.StringVar()
        self.tema_combo = ttk.Combobox(self.opcoes_frame, textvariable=self.tema_var, values=self.temas,
                                       state="readonly", width=15)
        self.tema_combo.set("darkly")  # Tema inicial
        self.tema_combo.pack(side=RIGHT)
        self.tema_combo.bind("<<ComboboxSelected>>", self.mudar_tema)

        # Frame para os botões
        self.botoes_frame = ttk.Frame(self.frame)
        self.botoes_frame.pack(pady=20, fill=X)

        # Botão Enviar
        self.enviar_btn = ttk.Button(self.botoes_frame, text="Enviar", bootstyle="success", command=self.enviar)
        self.enviar_btn.pack(side=LEFT, expand=True)

        # Botão Cancelar
        self.cancelar_btn = ttk.Button(self.botoes_frame, text="Cancelar", bootstyle="danger", command=self.cancelar)
        self.cancelar_btn.pack(side=LEFT, expand=True)

        # Frame para exibir os dados coletados
        self.dados_frame = ttk.Frame(self.frame)
        self.dados_frame.pack(pady=10, fill=X)

        # Labels para exibir os dados
        self.nome_label = ttk.Label(self.dados_frame, text="", anchor=CENTER)
        self.nome_label.pack(fill=X)

        self.email_label = ttk.Label(self.dados_frame, text="", anchor=CENTER)
        self.email_label.pack(fill=X)

        self.idade_label = ttk.Label(self.dados_frame, text="", anchor=CENTER)
        self.idade_label.pack(fill=X)

        self.lembrar_label = ttk.Label(self.dados_frame, text="", anchor=CENTER)
        self.lembrar_label.pack(fill=X)

    def set_icon(self):
        icon_ico = resource_path("logo.ico")
        icon_png = resource_path("logo.png")

        if os.path.exists(icon_ico):
            self.master.iconbitmap(icon_ico)
        elif os.path.exists(icon_png):
            logo = Image.open(icon_png)
            logo = ImageTk.PhotoImage(logo)
            self.master.iconphoto(True, logo)
        else:
            print("Arquivo de ícone não encontrado.")

    def enviar(self):
        # Atualiza as Labels com os dados coletados
        self.nome_label.config(text=f"Nome: {self.nome_entry.get()}")
        self.email_label.config(text=f"Email: {self.email_entry.get()}")
        self.idade_label.config(text=f"Idade: {self.idade_entry.get()}")
        # Atualiza o status do Checkbox Lembrar dados
        self.lembrar_label.config(text=f"Lembrar dados: {'Sim' if self.lembrar_var.get() else 'Não'}")

    def cancelar(self):
        # Limpa os campos de entrada e as labels
        self.nome_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.idade_entry.delete(0, END)
        self.lembrar_var.set(False)

        self.nome_label.config(text="")
        self.email_label.config(text="")
        self.idade_label.config(text="")
        self.lembrar_label.config(text="")

    def mudar_tema(self, event):
        # Função para mudar o tema quando um novo é selecionado no ComboBox
        novo_tema = self.tema_var.get()
        self.style.theme_use(novo_tema)

if __name__ == "__main__":
    root = ttk.Window()
    app = FormularioInscricao(root)
    root.mainloop()