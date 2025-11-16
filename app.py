from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys

# Função para carregar ícones redimensionados
def carregar_icone(nome, tamanho=(128,128)):
    img = Image.open(f"icones/{nome}")
    img = img.resize(tamanho, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

tela = Tk()
tela.title("Tela de Opções")
tela.geometry("1000x700")
tela.resizable(False, False)

# -------------------------
# BACKGROUND
# -------------------------
bg_image = Image.open("icones/bg_py.png")
bg_image = bg_image.resize((1000, 700), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

lbl_bg = Label(tela, image=bg_photo)
lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

# -------------------------
# Funções de navegação
# -------------------------
def abrir_tela_pessoas():
    subprocess.run([sys.executable, "pessoas.py"])

def abrir_tela_carros():
    subprocess.run([sys.executable, "carros.py"])

def abrir_tela_lugares():
    subprocess.run([sys.executable, "lugaresTuristicos.py"])

# -------------------------
# ÍCONES REDIMENSIONADOS
# -------------------------
img_pessoas = carregar_icone("logo_usuarios.png")
img_carros = carregar_icone("logo_carro.png")
img_lugares = carregar_icone("logo_loc.png")

# -------------------------
# FRAME CENTRALIZADO
# -------------------------

frame_botoes = Frame(tela, bg="", highlightthickness=0)
frame_botoes.place(relx=0.5, rely=0.5, anchor=CENTER)

# -------------------------
# BOTÕES
# -------------------------

btn_pessoas = Button(
    frame_botoes, text="Pessoas", image=img_pessoas, compound=TOP,
    bg="#FFFFFF", font="Cambria 12", fg="#0E0E0E",
    bd=2, relief="raised", padx=10, pady=10,
    command=abrir_tela_pessoas
)
btn_pessoas.pack(side=LEFT, padx=25)

btn_carros = Button(
    frame_botoes, text="Carros", image=img_carros, compound=TOP,
    bg="#FFFFFF", font="Cambria 12", fg="#0E0E0E",
    bd=2, relief="raised", padx=10, pady=10,
    command=abrir_tela_carros
)
btn_carros.pack(side=LEFT, padx=25)

btn_lugares = Button(
    frame_botoes, text="Lugares Turísticos", image=img_lugares, compound=TOP,
    bg="#FFFFFF", font="Cambria 12", fg="#0E0E0E",
    bd=2, relief="raised", padx=10, pady=10,
    command=abrir_tela_lugares
)
btn_lugares.pack(side=LEFT, padx=25)

tela.mainloop()
