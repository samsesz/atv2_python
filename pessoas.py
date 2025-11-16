from tkinter.ttk import *
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import pymongo
import tkinter as tk
from tkinter import messagebox

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
tela.title("Sistema Pessoas")
tela.geometry("950x500")
tela.configure(background="#F4F4F9")

# IMAGEM p_pessoa.png reduzida no cantinho
try:
    img_pessoa_original = PhotoImage(file="icones/p_pessoa.png")
    img_pessoa = img_pessoa_original.subsample(3, 3)
    lbl_pessoa_icon = Label(tela, image=img_pessoa, bg="#F4F4F9")
    lbl_pessoa_icon.place(x=5, y=5)
except Exception:
    # se não achar a imagem, ignora
    lbl_pessoa_icon = Label(tela, bg="#F4F4F9")
    lbl_pessoa_icon.place(x=5, y=5)

# Área onde a imagem selecionada aparece
lbl_imagem = Label(tela, background="#F4F4F9")
lbl_imagem.place(x=10, y=50)

# Botão escolher imagem
btn_escolher = Button(tela, text="Escolher imagem", command=escolher_imagem,
                      bg="#F4F4F9", fg="#333333", font="cambria 12 bold")
btn_escolher.place(x=10, y=200)

# Conexão com o MongoDB
atv2 = pymongo.MongoClient("mongodb://localhost:27017")
db = atv2["atv2py"]
collection = db["pessoas"]

# Labels e Entradas – ID
Label(tela, text="ID:", bg="#F4F4F9", font=("Cambria", 12), fg="#0E0E0E").place(x=160, y=50)
campo_id = Entry(tela, width=30, bg="white", fg="#0E0E0E", borderwidth=5)
campo_id.place(x=240, y=50)

# Nome
Label(tela, text="Nome:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=100)
campo_nome = Entry(tela, width=30, bg="white", fg="#0E0E0E", borderwidth=5)
campo_nome.place(x=240, y=100)

# Nascimento
Label(tela, text="Nascimento:", bg="#F4F4F9", font=("Cambria", 12)).place(x=550, y=100)
campo_nasc = Entry(tela, width=30, bg="#FFF", fg="#333", borderwidth=4)
campo_nasc.place(x=680, y=100)

# Idade
Label(tela, text="Idade:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=150)
campo_idade = Entry(tela, width=30, bg="#FFF", fg="#333", borderwidth=4)
campo_idade.place(x=240, y=150)

# Telefone
Label(tela, text="Telefone:", bg="#F4F4F9", font=("Cambria", 12)).place(x=550, y=200)
campo_tel = Entry(tela, width=30, bg="#FFF", fg="#333", borderwidth=4)
campo_tel.place(x=680, y=200)

# Altura
Label(tela, text="Altura:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=200)
campo_altura = Entry(tela, width=30, bg="#FFF", fg="#333", borderwidth=4)
campo_altura.place(x=240, y=200)

# Peso
Label(tela, text="Peso:", bg="#F4F4F9", font=("Cambria", 12)).place(x=550, y=150)
campo_peso = Entry(tela, width=30, bg="#FFF", fg="#333", borderwidth=4)
campo_peso.place(x=680, y=150)

# Gênero
genero_var = StringVar(value="M")
Label(tela, text="Gênero:", bg="#F4F4F9", font=("Cambria", 12)).place(x=550, y=250)
Radiobutton(tela, text="M", variable=genero_var, value="M", bg="#F4F4F9").place(x=680, y=250)
Radiobutton(tela, text="F", variable=genero_var, value="F", bg="#F4F4F9").place(x=740, y=250)

# Cidade
Label(tela, text="Cidade:", bg="#F4F4F9", font=("Cambria", 12)).place(x=160, y=250)
seleciona_cidade = Combobox(tela, width=29)
seleciona_cidade["values"] = ("São Paulo", "Santos", "Curitiba", "Florianópolis", "Cuiabá")
seleciona_cidade.current(0)
seleciona_cidade.place(x=240, y=250)

# Label para exibir informações
info_pessoa = Label(tela, text="", font=("Cambria", 12), fg="#333")
info_pessoa.place(x=70, y=380)

lbl_mensagem = Label(tela, text="", bg="#fff")
lbl_mensagem.place(x=490, y=410)

# ------------------ Funções ------------------ #

def limpar_campos_pessoa():
    campo_id.delete(0, tk.END)
    campo_nome.delete(0, tk.END)
    campo_nasc.delete(0, tk.END)
    campo_idade.delete(0, tk.END)
    campo_tel.delete(0, tk.END)
    campo_altura.delete(0, tk.END)
    campo_peso.delete(0, tk.END)
    seleciona_cidade.set("")

def salvar_pessoa():
    # valida idade
    idade_val = 0
    idade_text = campo_idade.get().strip()
    if idade_text:
        try:
            idade_val = int(idade_text)
        except ValueError:
            messagebox.showerror("Erro", "Idade inválida. Informe um número.")
            return

    dados = {
        "id": campo_id.get().strip(),
        "nome": campo_nome.get().strip(),
        "nasc": campo_nasc.get().strip(),
        "idade": idade_val,
        "telefone": campo_tel.get().strip(),
        "altura": campo_altura.get().strip(),
        "peso": campo_peso.get().strip(),
        "cidade": seleciona_cidade.get()
    }

    if not dados["id"]:
        messagebox.showwarning("Atenção", "Preencha o ID antes de salvar.")
        return

    collection.insert_one(dados)
    lbl_mensagem.config(text="Registro salvo com sucesso.", fg="green")

    info_pessoa.config(text=(
        f"Dados da Pessoa:\n"
        f"ID: {dados['id']}\n"
        f"Nome: {dados['nome']}\n"
        f"Data de Nascimento: {dados['nasc']}\n"
        f"Idade: {dados['idade']}\n"
        f"Telefone: {dados['telefone']}\n"
        f"Altura: {dados['altura']}\n"
        f"Peso: {dados['peso']}\n"
        f"Cidade: {dados['cidade']}"
    ))

    limpar_campos_pessoa()

def consultar_pessoa():
    if not campo_id.get().strip():
        messagebox.showwarning("Atenção", "Informe o ID para consultar.")
        return
    registro = collection.find_one({"id": campo_id.get().strip()})
    if registro:
        # limpa antes de inserir
        limpar_campos_pessoa()
        campo_id.insert(0, registro.get("id", ""))
        campo_nome.insert(0, registro.get("nome", ""))
        campo_nasc.insert(0, registro.get("nasc", ""))
        campo_idade.insert(0, str(registro.get("idade", "")))
        campo_tel.insert(0, registro.get("telefone", ""))
        campo_altura.insert(0, registro.get("altura", ""))
        campo_peso.insert(0, registro.get("peso", ""))
        seleciona_cidade.set(registro.get("cidade", ""))
        lbl_mensagem.config(text="Registro encontrado.", fg="green")
    else:
        lbl_mensagem.config(text="Registro não encontrado.", fg="red")

def atualizar_pessoa():
    id_busca = campo_id.get().strip()
    if not id_busca:
        messagebox.showwarning("Atenção", "Informe o ID para alterar.")
        return

    registro = collection.find_one({"id": id_busca})
    if not registro:
        messagebox.showerror("Erro", "Registro não encontrado para atualizar.")
        return

    # valida idade
    idade_val = 0
    idade_text = campo_idade.get().strip()
    if idade_text:
        try:
            idade_val = int(idade_text)
        except ValueError:
            messagebox.showerror("Erro", "Idade inválida. Informe um número.")
            return

    novos_valores = {
        "nome": campo_nome.get().strip(),
        "nasc": campo_nasc.get().strip(),
        "idade": idade_val,
        "telefone": campo_tel.get().strip(),
        "altura": campo_altura.get().strip(),
        "peso": campo_peso.get().strip(),
        "cidade": seleciona_cidade.get()
    }

    collection.update_one({"id": id_busca}, {"$set": novos_valores})
    lbl_mensagem.config(text="Atualizado com sucesso.", fg="green")
     # limpa informação mostrada
    info_pessoa.config(text="")
    limpar_campos_pessoa()

def excluir_pessoa():
    id_remove = campo_id.get().strip()
    if not id_remove:
        messagebox.showwarning("Atenção", "Informe o ID para excluir.")
        return

    registro = collection.find_one({"id": id_remove})
    if not registro:
        messagebox.showerror("Erro", "Registro não encontrado para excluir.")
        return

    confirma = messagebox.askyesno("Confirmar", f"Excluir registro ID {id_remove}?")
    if confirma:
        collection.delete_one({"id": id_remove})
        lbl_mensagem.config(text="Registro excluído.", fg="green")
        info_pessoa.config(text="")
        
        limpar_campos_pessoa()

# ------- BOTÕES ------- #

foto_salvar = PhotoImage(file="icones/salvar.png")
foto_excluir = PhotoImage(file="icones/excluir.png")
foto_alterar = PhotoImage(file="icones/alterar.png")
foto_consultar = PhotoImage(file="icones/consultar.png")
foto_sair = PhotoImage(file="icones/sair.png")

Button(tela, image=foto_salvar, command=salvar_pessoa).place(x=240, y=310)
Button(tela, image=foto_excluir, command=excluir_pessoa).place(x=320, y=310)
Button(tela, image=foto_alterar, command=atualizar_pessoa).place(x=400, y=310)
Button(tela, image=foto_consultar, command=consultar_pessoa).place(x=480, y=310)
Button(tela, image=foto_sair, command=tela.quit).place(x=560, y=310)

# Textos abaixo dos botões
Label(tela, text="Salvar", bg="#F4F4F9", font=("Cambria", 10)).place(x=250, y=372)
Label(tela, text="Excluir", bg="#F4F4F9", font=("Cambria", 10)).place(x=330, y=372)
Label(tela, text="Alterar", bg="#F4F4F9", font=("Cambria", 10)).place(x=410, y=372)
Label(tela, text="Consultar", bg="#F4F4F9", font=("Cambria", 10)).place(x=480, y=372)
Label(tela, text="Sair", bg="#F4F4F9", font=("Cambria", 10)).place(x=570, y=372)

tela.mainloop()
