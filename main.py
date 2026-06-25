#Creado por: Alejandro Sibaja Badilla y Marco Herrera Gómez
#Fecha de creación: 18/06/26
#Ultima modificación:
#Versión de python: 3.14

import customtkinter as ctk
from funciones import *
from archivos import *
from clases import *
def abrirVentanaPrincipal():
    ventana=ctk.CTk()
    ventana.title("Sistema de Parqueo")
    ventana.geometry("600x500")
    titulo=ctk.CTkLabel(
        ventana,
        text="SISTEMA DE PARQUEO",
        font=("Arial",24,"bold")
    )
    titulo.pack(pady=30)
    ventana.mainloop()

abrirVentanaPrincipal()