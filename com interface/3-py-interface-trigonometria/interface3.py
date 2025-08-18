import tkinter as tk  # Importa a biblioteca Tkinter para a criação da interface gráfica
import math  # Importa a biblioteca math para realizar operações matemáticas
from PIL import Image, ImageTk  # Importa as classes Image e ImageTk da biblioteca PIL para manipulação de imagens
import os  # Importa a biblioteca os para operações com o sistema de arquivos
import sys  # Importa a biblioteca sys para manipulação de variáveis e funções do sistema

def resource_path(relative_path):
    """
    Obtém o caminho absoluto para o recurso, funciona tanto em ambiente de desenvolvimento
    quanto após o empacotamento com PyInstaller.
    """
    try:
        # PyInstaller cria um diretório temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver executando pelo PyInstaller, utiliza o caminho absoluto do diretório atual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)  # Retorna o caminho completo do arquivo

def calcular():
    """
    Realiza o cálculo dos valores trigonométricos (seno, cosseno e tangente) do ângulo fornecido
    e atualiza os labels com os resultados.
    """
    try:
        angulo = float(entrada_angulo.get())  # Obtém o valor do ângulo inserido pelo usuário
        radiano = math.radians(angulo)  # Converte o ângulo de graus para radianos

        # Calcula os valores trigonométricos
        seno = math.sin(radiano)
        cosseno = math.cos(radiano)
        tangente = math.tan(radiano)

        # Atualiza os labels com os resultados formatados com 3 casas decimais
        resultado_seno.config(text=f"{seno:.3f}")
        resultado_cosseno.config(text=f"{cosseno:.3f}")
        resultado_tangente.config(text=f"{tangente:.3f}")
    except ValueError:
        # Em caso de erro (por exemplo, entrada inválida), exibe "Erro" nas labels
        resultado_seno.config(text="Erro")
        resultado_cosseno.config(text="Erro")
        resultado_tangente.config(text="Erro")

def limpar():
    """
    Limpa a entrada do usuário e reseta as labels dos resultados.
    """
    entrada_angulo.delete(0, tk.END)  # Limpa o campo de entrada
    resultado_seno.config(text="")  # Limpa o resultado do seno
    resultado_cosseno.config(text="")  # Limpa o resultado do cosseno
    resultado_tangente.config(text="")  # Limpa o resultado da tangente

def validar_entrada(texto):
    """
    Valida a entrada do usuário permitindo apenas números e garantindo que o valor esteja entre 0 e 90.
    """
    if texto.isdigit() or texto == "":  # Permite apenas números ou campo vazio
        if texto == "":  # Se o campo estiver vazio, permite a entrada
            return True
        valor = int(texto)  # Converte o texto para inteiro
        return 0 <= valor <= 90  # Retorna True se o valor estiver entre 0 e 90, caso contrário False
    return False  # Se o texto não for um número, retorna False

# Configuração da janela principal
janela = tk.Tk()  # Cria a janela principal
janela.title("Calculadora Trigonométrica")  # Define o título da janela
janela.geometry("400x550")  # Define o tamanho da janela
janela.configure(bg="#f0f0f0")  # Define a cor de fundo da janela

# Carregar e definir o ícone da janela
try:
    icone_path = resource_path("seno.png")  # Obtém o caminho da imagem do ícone
    icone = Image.open(icone_path)  # Abre a imagem do ícone
    icone = ImageTk.PhotoImage(icone)  # Converte a imagem para um formato compatível com Tkinter
    janela.iconphoto(True, icone)  # Define a imagem como ícone da janela
except FileNotFoundError:
    print("Imagem 'seno.png' não encontrada para o ícone")  # Caso o arquivo não seja encontrado, exibe uma mensagem de erro

# Imagem seno2.png
try:
    imagem_path = resource_path("seno2.png")  # Obtém o caminho da imagem principal
    imagem = Image.open(imagem_path)  # Abre a imagem
    imagem = imagem.resize((380, 200), Image.LANCZOS)  # Redimensiona a imagem
    foto = ImageTk.PhotoImage(imagem)  # Converte a imagem para um formato compatível com Tkinter
    label_imagem = tk.Label(janela, image=foto, bg="#f0f0f0", borderwidth=0)  # Cria um label para exibir a imagem
    label_imagem.image = foto  # Mantém uma referência da imagem para evitar que o garbage collector a remova
    label_imagem.pack(pady=20)  # Posiciona a imagem na janela
except FileNotFoundError:
    # Caso a imagem não seja encontrada, exibe uma mensagem de texto no lugar da imagem
    label_imagem = tk.Label(janela, text="Imagem 'seno2.png' não encontrada", bg="#f0f0f0")
    label_imagem.pack(pady=20)

# Entrada do ângulo
frame_entrada = tk.Frame(janela, bg="#f0f0f0")  # Cria um frame para organizar a entrada
frame_entrada.pack(pady=10)  # Posiciona o frame na janela com um espaçamento vertical

label_angulo = tk.Label(frame_entrada, text="Ângulo (0 à 90):", font=('Arial', 14), bg="#f0f0f0")  # Label para o campo de entrada
label_angulo.pack(pady=(0, 5))  # Posiciona o label com um pequeno espaçamento inferior

validacao = janela.register(validar_entrada)  # Registra a função de validação para a entrada
entrada_angulo = tk.Entry(frame_entrada, width=3,justify='center', font=('Arial', 16),
                          bd=0 , highlightthickness=0, relief='flat', bg="#f0f0f0", fg='red',
                          validate="key", validatecommand=(validacao, "%P"))  # Cria o campo de entrada do ângulo
entrada_angulo.pack()  # Posiciona o campo de entrada

# Linha abaixo do campo de entrada
linha = tk.Frame(frame_entrada, bg="black", height=1, width=entrada_angulo.winfo_reqheight())  # Cria uma linha decorativo abaixo do campo de entrada
linha.pack(pady=(0, 5))  # Posiciona a linha com um pequeno espaçamento inferior 

# Botões
frame_botoes = tk.Frame(janela, bg="#f0f0f0")  # Cria um frame para organizar os botões
frame_botoes.pack(pady=20) # Posiciona o frame na janela com um espaçamento

botao_calcular = tk.Button(frame_botoes, text="Calcular", command=calcular, font=('Arial', 12),
                            bg="#d9d9d9", relief='flat',bd=0, highlightthickness=0) # Botão para calcular os valores trigonométricos
botao_calcular.pack(side=tk.LEFT, padx=10) # Posiciona o botão à esquerda com um espaçamento horizontal

botao_limpar = tk.Button(frame_botoes, text="Limpar", command=limpar, font=('Arial', 12), 
                        bg="#d9d9d9", relief='flat', bd=0, highlightthickness=0) # Botão para limpar a entrada e os resultados
botao_limpar.pack(side=tk.RIGHT, padx=10) # Posiciona o botão à direita com um espaçamento horizontal 

# Resultados
frame_resultados = tk.Frame(janela, bg="#f0f0f0") # Cria um frame para organizar os resultados 
frame_resultados.pack(pady=10) # Posiciona o frame na janela com um espaçamento vertical

# Label e resultado para o Seno
label_seno = tk.Label(frame_resultados, text="Seno:", font=('Arial', 12), bg="#f0f0f0")
label_seno.grid(row=0, column=0, padx=10, pady=5, sticky="e") # Label para o seno alinhado à direita
resultado_seno = tk.Label(frame_resultados, text="", font=('Arial', 12, 'bold'), fg="red", bg="#f0f0f0")
resultado_seno.grid(row=0, column=1, padx=10, pady=5, sticky="w") # Label que exibe o resultado do seno, alinhado à esquerda

# Label e resultado para o Cosseno
label_cosseno = tk.Label(frame_resultados, text="Cosseno:", font=('Arial', 12), bg="#f0f0f0")
label_cosseno.grid(row=1, column=0, padx=10, pady=5, sticky="e") # Label para o cosseno, alinhado à direita
resultado_cosseno = tk.Label(frame_resultados, text="", font=('Arial', 12, 'bold'),fg='red', bg="#f0f0f0")
resultado_cosseno.grid(row=1, column=1, padx=10, pady=5, sticky="w") # Label que exibe o resultado do cosseno, alinhado à esquerda

# Label e resultado para a Tangente
label_tangente = tk.Label (frame_resultados, text="Tangente:", font= ('Arial', 12), bg="#f0f0f0" )
label_tangente.grid(row=2, column=0, padx=10, pady=5, sticky='e') # Label para a tangente alinhado à direita
resultado_tangente = tk.Label(frame_resultados, text="", font=('Arial', 12,'bold'), fg='red', bg="#f0f0f0")
resultado_tangente.grid (row=2, column=1, padx=10,pady=5, sticky='w') # Label que exibe o resultado da tangente, alinhado à esquerda

# Iniciar a janela
janela.mainloop() # Inicia o loop principal da aplicação, mantendo a janela aberta