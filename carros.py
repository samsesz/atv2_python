from tkinter.ttk import *
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import pymongo
import tkinter as tk

# Função para escolher imagem
def escolher_imagem():
    pasta_inicial = ""
    caminho_imagem = filedialog.askopenfilename(
        initialdir=pasta_inicial,
        title="Escolha uma imagem",
        filetypes=(("Arquivos de imagem", "*.jpg;*.jpeg;*.png"), ("Todos os arquivos", "*.*"))
    )
    if not caminho_imagem:
        return
    try:
        imagem_pil = Image.open(caminho_imagem)
        largura, altura = imagem_pil.size
        if largura > 150:
            proporcao = largura / 150
            nova_altura = int(altura / proporcao)
            imagem_pil = imagem_pil.resize((150, nova_altura))
        imagem_tk = ImageTk.PhotoImage(imagem_pil)
        lbl_imagem.config(image=imagem_tk)
        lbl_imagem.image = imagem_tk
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")

# Configuração da tela
tela = Tk()
tela.title("Sistema de Carros")
tela.geometry("950x500")
tela.configure(background="#a5a201")

# IMAGEM carro.jpeg acima do botão
img_carro_original = PhotoImage(file="icones/carro.png")
img_carro = img_carro_original.subsample(4, 4)
lbl_carro_icon = Label(tela, image=img_carro, bg="#F4F4F9")
lbl_carro_icon.place(x=5, y=5)

# Área onde a imagem escolhida aparece
lbl_imagem = Label(tela, background="#F4F4F9")
lbl_imagem.place(x=10, y=50)

# Botão escolher imagem
btn_escolher = Button(tela, text="Escolher imagem", command=escolher_imagem,
                      bg="#F4F4F9", fg="#333333", font="cambria 12 bold")
btn_escolher.place(x=10, y=200)

# Conexão com o MongoDB
atv2 = pymongo.MongoClient("mongodb://localhost:27017")
db = atv2["atv2py"]
collection = db["carros"]

# ------- CAMPOS ------- #

# Código
Label(tela, text="Código:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=50)
campo_codigo = Entry(tela, width=30, bg="white", fg="#0E0E0E", borderwidth=5)
campo_codigo.place(x=240, y=50)

# Nome do veículo
Label(tela, text="Nome:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=100)
campo_nome = Entry(tela, width=30, bg="white", fg="#0E0E0E", borderwidth=5)
campo_nome.place(x=240, y=100)

# Placa
Label(tela, text="Placa:", bg="#F4F4F9", font=("Cambria", 12)).place(x=550, y=100)
campo_placa = Entry(tela, width=30, bg="#FFF", fg="#333", borderwidth=4)
campo_placa.place(x=680, y=100)

# Modelo
Label(tela, text="Modelo:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=150)
campo_modelo = Entry(tela, width=30, bg="#FFF", fg="#333", borderwidth=4)
campo_modelo.place(x=240, y=150)

# Utilitário / Não Utilitário
Label(tela, text="Utilitário:", bg="#F4F4F9", font=("Cambria", 12)).place(x=550, y=150)
util_var = StringVar(value="Não")
Radiobutton(tela, text="Sim", variable=util_var, value="Sim", bg="#F4F4F9").place(x=680, y=150)
Radiobutton(tela, text="Não", variable=util_var, value="Não", bg="#F4F4F9").place(x=740, y=150)

# Marca (Combobox)
Label(tela, text="Marca:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=200)
campo_marca = Combobox(tela, width=29)
campo_marca["values"] = ("Chevrolet", "Fiat", "Suzuki", "Volkswagen", "Renault", "Ford")
campo_marca.current(0)
campo_marca.place(x=240, y=200)

# Exibe informações
info_carro = Label(tela, text="", font=("Cambria", 12), fg="#333")
info_carro.place(x=70, y=380)

# ------- FUNÇÕES ------- #

def limpar_campos():
    campo_codigo.delete(0, tk.END)
    campo_nome.delete(0, tk.END)
    campo_placa.delete(0, tk.END)
    campo_modelo.delete(0, tk.END)
    campo_marca.set("")

def salvar():
    dados = {
        "codigo": campo_codigo.get(),
        "nome": campo_nome.get(),
        "placa": campo_placa.get(),
        "modelo": campo_modelo.get(),
        "utilitario": util_var.get(),
        "marca": campo_marca.get()
    }

    collection.insert_one(dados)

    info_carro.config(text=(
        f"Dados do Carro:\n"
        f"Código: {dados['codigo']}\n"
        f"Nome: {dados['nome']}\n"
        f"Placa: {dados['placa']}\n"
        f"Modelo: {dados['modelo']}\n"
        f"Utilitário: {dados['utilitario']}\n"
        f"Marca: {dados['marca']}"
    ))

    limpar_campos()

def atualizar():
    codigo_busca = campo_codigo.get()

    novos_valores = {
        "nome": campo_nome.get(),
        "placa": campo_placa.get(),
        "modelo": campo_modelo.get(),
        "utilitario": util_var.get(),
        "marca": campo_marca.get()
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
        campo_placa.insert(0, registro["placa"])
        campo_modelo.insert(0, registro["modelo"])
        util_var.set(registro["utilitario"])
        campo_marca.set(registro["marca"])
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
