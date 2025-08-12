# Usando biblioteca Tkinter (Padrão Python para interfaces)
import tkinter as tk

# Submódulo do Tkinter com widgets mais modernos e estilizados
from tkinter import ttk

def atualizar_resultado():
    # Obter o texto da caixa de entrada
    nome = caixa_texto.get()

    # Obter a opção selecionada nos botões de rádio
    preferencia = var_radio.get()

    # Verificar se a caixa de seleção de saudação
    # informal esta marcada
    if var_check_saudacao.get():
        saudacao = "Olá"
    else:
        saudacao = "Bem-vindo"

    # Verificar se a caixa de seleção de saudação
    # personalizada esta marcada
    if var_check_personalizada.get():
        saudacao = f"{saudacao}, caro(a)"

    # Obter a cor favorita selecionada
    cor_favorita = combo_cor.get() 

    # Montar mensagem final
    mensagem = f"{saudacao} {nome}!\nVocê prefere {preferencia}. "
    if cor_favorita:
        mensagem += f"Sua cor favorita é: {cor_favorita}. "

    # Atualizar o texto do rótulo de mensagem
    label_resultado.config(text=mensagem)

def limpar_campos():
    # Limpa todas as escolhas
    caixa_texto.delete(0, tk.END)
    var_radio.set("Café")
    var_check_saudacao.set(False)
    var_check_personalizada.set(False)
    combo_cor.set("Escolha (sua cor)")
    label_resultado.config(text="")

# Criar a janela principal
janela = tk.Tk()
janela.title("Interface avançada")
janela.geometry("400x500")

# Criar uma caixa de entrada (Entry)
label_nome = tk.Label(janela, text="Digite seu nome:")
label_nome.pack(pady=5)
caixa_texto = tk.Entry(janela, width=40)
caixa_texto.pack(pady=5)

# Criar botões de rádio
label_preferencia = tk.Label(janela, text=" Escolha sua preferência:")
label_preferencia.pack(pady=5)

var_radio = tk.StringVar(value="Café")
radio_cafe = tk.Radiobutton(janela, text="Café", variable=var_radio, value="Café")
radio_cha = tk.Radiobutton(janela, text="Chá", variable=var_radio, value="Chá")
radio_suco = tk.Radiobutton(janela, text="Suco", variable=var_radio, value="Suco")
radio_agua = tk.Radiobutton(janela, text="Água", variable=var_radio, value="Água")

# .pack (Método do Tkinter que
# deixa as opções visíveis)
radio_cafe.pack()
radio_cha.pack()
radio_suco.pack()
radio_agua.pack()

# Criar caixas de seleção múltipla (Checkbox)
var_check_saudacao = tk.BooleanVar()
check_saudacao =tk.Checkbutton(janela, text="Usar saudação informal", variable=var_check_saudacao)
check_saudacao.pack(pady=5)

var_check_personalizada = tk.BooleanVar()
check_personalizada =tk.Checkbutton(janela, text="Usar saudação personalizada", variable=var_check_personalizada)
check_personalizada.pack(pady=5)

# ComboBox (Caixa de seleção com opções)
label_cor = tk.Label(janela, text="Escolha sua cor favorita:")
label_cor.pack(pady=5)

combo_cor = ttk.Combobox(janela, values=["Vermelho","Azul","Verde","Amarelo","Preto","Branco"])
combo_cor.set("Escolha (sua cor)")
combo_cor.pack(pady=5)

# Criar botões (Frase e Limpar)
botao_atualizar = tk.Button(janela, text="Atualizar", command=atualizar_resultado)
botao_atualizar.pack(pady=10)

botao_limpar = tk.Button(janela, text="Limpar", command=limpar_campos)
botao_limpar.pack(pady=10)

# Exibição do resultado final (Rótulo "Label")
label_resultado = tk.Label(janela, text="", wraplength=300)
label_resultado.pack(pady=10)

# Executar a janela principal
janela.mainloop()

 