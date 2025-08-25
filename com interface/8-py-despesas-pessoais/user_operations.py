from tkinter import messagebox

# Inicializa a classe com referências ao banco de dados e à interface do usuário.
class UserOperations:
    def __init__(self, db, ui):
        self.db = db
        self.ui = ui

    # Cadastra um novo usuário no banco de dados
    def cadastrar(self):
        nome = self.ui.nome_entry.get()
        if nome:
            self.db.insert_user(nome)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.ui.nome_entry.delete(0, 'end')
            self.ui.carregar_dados()
        else:
            messagebox.showerror("Erro", "Por favor, preencha o campo Nome.")

    # Atualiza as informações de um usuário existente
    def atualizar_usuario(self):
        if self.ui.selected_user:
            novo_nome = self.ui.nome_entry.get()
            if novo_nome:
                self.db.update_user(self.ui.selected_user[0], novo_nome)
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
                self.ui.carregar_dados()
                self.ui.nome_entry.delete(0, 'end')
                self.ui.selected_user = None
            else:
                messagebox.showerror("Erro", "Por favor, preencha o campo Nome.")
        else:
            messagebox.showerror("Erro", "Por favor, selecione um usuário para atualizar.")

    # Exclui um usuário do banco de dados
    def excluir_usuario(self):
        if self.ui.selected_user:
            if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este usuário?"):
                self.db.delete_user(self.ui.selected_user[0])
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                self.ui.carregar_dados()
                self.ui.nome_entry.delete(0, 'end')
                self.ui.selected_user = None
        else:
            messagebox.showerror("Erro", "Por favor, selecione um usuário para excluir.")
