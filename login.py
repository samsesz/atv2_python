from tkinter import *
from tkinter import messagebox
import subprocess

# Configurações da login de login
login = Tk()
lbl_imagem = Label(login, background="#FFFFFF")
lbl_imagem.place(x=30, y=70)
login.configure(background="#FFFFFF")
login.title("Acesso ao sistema")
login.geometry("400x200")
login.resizable(True, True)

# Usuario
Label(login, text="Usuario", bg="#FFFFFF").place(x=50, y=70)
txt_user = Entry(login, width=20)
txt_user.place(x=100, y=70)

# Senha
Label(login, text="Senha", bg="#FFFFFF").place(x=50, y=110) 
txt_senha = Entry(login, width=20)
txt_senha.place(x=100, y=110) 

# Função para sair do sistema
def sair():
    resposta = messagebox.askquestion("sair do sistema?", "Deseja mesmo sair do sistema?")
    if resposta == "yes":
        login.destroy()

# Função para validação de acesso
def validar_acesso(usuario, senha):
    if usuario == "admin" and senha == "123":
        abrir_app()
    else:
        messagebox.showerror("Acesso negado", "Usuário ou senha incorretos.")

# Função de menu principal
def abrir_app():
    login.destroy()
    subprocess.run(["python", "app.py"])

# Função do botão de acessar
def click_botao():
    usuario = txt_user.get()
    senha = txt_senha.get()
    validar_acesso(usuario, senha)

# Imagens dos botões
foto_acesso = PhotoImage(file="icones/acesso.png")
foto_logout = PhotoImage(file="icones/sair.png")

# Criação dos botões
# Botão acesso
btn_usuario = Button(login, text= "Acessar", image=foto_acesso, compound=TOP, command=click_botao)
btn_usuario.place(x=250, y=65)

# Botão sair
btn_sair = Button(login, text="Sair", image=foto_logout, compound=TOP, command=sair)
btn_sair.place(x=320, y=65)

# Organização da login
largura_screen = login.winfo_screenwidth()
altura_screen = login.winfo_screenheight()

login.mainloop()