from tkinter.ttk import *
from tkinter import *
import pymongo
import tkinter as tk
from PIL import Image, ImageTk

# Configuração da tela
tela = Tk()
tela.title("Sistema de Lugares Turísticos")
tela.geometry("950x500")
tela.configure(background="#244B26")

# IMAGEM fixa (louvre.png) no lugar da foto
img_louvre_original = Image.open("icones/louvre.png")
img_louvre_original = img_louvre_original.resize((150, 100))  # Ajuste de tamanho
img_louvre = ImageTk.PhotoImage(img_louvre_original)

lbl_imagem = Label(tela, image=img_louvre, bg="#F4F4F9")
lbl_imagem.place(x=10, y=50)

# Conexão com o MongoDB
atv2 = pymongo.MongoClient("mongodb://localhost:27017")
db = atv2["atv2py"]
collection = db["lugares"]

# ------- CAMPOS ------- #

# Código
Label(tela, text="Código:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=50)
campo_codigo = Entry(tela, width=30, bg="white", fg="#0E0E0E", borderwidth=5)
campo_codigo.place(x=240, y=50)

# Nome do local
Label(tela, text="Nome do Local:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=100)
campo_nome = Entry(tela, width=30, bg="white", fg="#0E0E0E", borderwidth=5)
campo_nome.place(x=300, y=100)

# Valor de entrada
Label(tela, text="Valor de Entrada:", bg="#F4F4F9", font=("Cambria", 12)).place(x=550, y=100)
campo_valor = Entry(tela, width=30, bg="#FFF", fg="#333", borderwidth=4)
campo_valor.place(x=680, y=100)

# Necessita guia (radio)
Label(tela, text="Necessita Guia:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=150)
guia_var = StringVar(value="Não")
Radiobutton(tela, text="Sim", variable=guia_var, value="Sim", bg="#F4F4F9").place(x=300, y=150)
Radiobutton(tela, text="Não", variable=guia_var, value="Não", bg="#F4F4F9").place(x=360, y=150)

# Cidade
Label(tela, text="Cidade:", bg="#F4F4F9", font=("Cambria", 12)).place(x=550, y=150)
campo_cidade = Entry(tela, width=30, bg="#FFF", fg="#333", borderwidth=4)
campo_cidade.place(x=680, y=150)

# Estado (combobox)
Label(tela, text="Estado:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=200)
campo_estado = Combobox(tela, width=29)
campo_estado["values"] = ("SP", "RJ", "MG", "BA", "RS")
campo_estado.current(0)
campo_estado.place(x=240, y=200)

# Exibe informações
info_local = Label(tela, text="", font=("Cambria", 12), fg="#333")
info_local.place(x=70, y=380)

# ------- FUNÇÕES ------- #

def limpar_campos():
    campo_codigo.delete(0, tk.END)
    campo_nome.delete(0, tk.END)
    campo_valor.delete(0, tk.END)
    campo_cidade.delete(0, tk.END)
    campo_estado.set("")
    guia_var.set("Não")

def salvar():
    dados = {
        "codigo": campo_codigo.get(),
        "nome": campo_nome.get(),
        "valor": campo_valor.get(),
        "guia": guia_var.get(),
        "cidade": campo_cidade.get(),
        "estado": campo_estado.get()
    }

    collection.insert_one(dados)

    info_local.config(text=(
        f"Local Turístico:\n"
        f"Código: {dados['codigo']}\n"
        f"Nome: {dados['nome']}\n"
        f"Entrada: {dados['valor']}\n"
        f"Guia: {dados['guia']}\n"
        f"Cidade: {dados['cidade']}\n"
        f"Estado: {dados['estado']}"
    ))

    limpar_campos()

def atualizar():
    codigo_busca = campo_codigo.get()

    novos_valores = {
        "nome": campo_nome.get(),
        "valor": campo_valor.get(),
        "guia": guia_var.get(),
        "cidade": campo_cidade.get(),
        "estado": campo_estado.get()
    }

    collection.update_one({"codigo": codigo_busca}, {"$set": novos_valores})
    limpar_campos()

def excluir():
    codigo_remove = campo_codigo.get()
    collection.delete_one({"codigo": codigo_remove})
    limpar_campos()

def consultar():
    registro = collection.find_one({"codigo": campo_codigo.get()})

    if registro:
        campo_nome.insert(0, registro["nome"])
        campo_valor.insert(0, registro["valor"])
        guia_var.set(registro["guia"])
        campo_cidade.insert(0, registro["cidade"])
        campo_estado.set(registro["estado"])
        lbl_mensagem.config(text="", fg="green")
    else:
        lbl_mensagem.config(text="Registro não encontrado.", fg="red")

lbl_mensagem = Label(tela, text="", bg="#fff")
lbl_mensagem.place(x=490, y=410)

# ------- BOTÕES ------- #

foto_salvar = PhotoImage(file="icones/salvar.png")
foto_excluir = PhotoImage(file="icones/excluir.png")
foto_alterar = PhotoImage(file="icones/alterar.png")
foto_consultar = PhotoImage(file="icones/consultar.png")
foto_sair = PhotoImage(file="icones/sair.png")

Button(tela, image=foto_salvar, command=salvar).place(x=240, y=310)
Button(tela, image=foto_excluir, command=excluir).place(x=320, y=310)
Button(tela, image=foto_alterar, command=atualizar).place(x=400, y=310)
Button(tela, image=foto_consultar, command=consultar).place(x=480, y=310)
Button(tela, image=foto_sair, command=tela.quit).place(x=560, y=310)

# Textos abaixo dos botões
Label(tela, text="Salvar", bg="#F4F4F9", font=("Cambria", 10)).place(x=250, y=372)
Label(tela, text="Excluir", bg="#F4F4F9", font=("Cambria", 10)).place(x=330, y=372)
Label(tela, text="Alterar", bg="#F4F4F9", font=("Cambria", 10)).place(x=410, y=372)
Label(tela, text="Consultar", bg="#F4F4F9", font=("Cambria", 10)).place(x=480, y=372)
Label(tela, text="Sair", bg="#F4F4F9", font=("Cambria", 10)).place(x=570, y=372)

tela.mainloop()
