#Creado por: Alejandro Sibaja Badilla y Marco Herrera Gómez
#Fecha de creación: 18/06/26
#Ultima modificación:
#Versión de python: 3.14

import customtkinter as ctk
from funciones import *
from archivos import *
from clases import *
from tkinter import messagebox
def acercaDe(ventanaPrincipal):
    """
    Funcionalidad:
    Muestra una ventana con la información de los desarrolladores del sistema.
    Entradas:
    -ventanaPrincipal(object):Ventana padre desde donde se invoca.
    Salidas:
    Ventana gráfica con datos del equipo de desarrollo.
    """
    ventanaAcerca=ctk.CTkToplevel(ventanaPrincipal)
    ventanaAcerca.title("Acerca de")
    ventanaAcerca.geometry("300x200")
    lblInfo=ctk.CTkLabel(ventanaAcerca,text="Desarrollado por:\nAlejandro Sibaja Badilla\nMarco Herrera Gómez")
    lblInfo.pack(pady=30)
    btnRegresar=ctk.CTkButton(ventanaAcerca,text="Regresar",command=ventanaAcerca.destroy)
    btnRegresar.pack()

def abrirVentanaPrincipal():
    baseDatos=cargarBD()
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("tema/midnight.json")
    ventana=ctk.CTk()
    ventana.title("Sistema de Parqueo")
    ventana.geometry("600x550")
    titulo=ctk.CTkLabel(
        ventana,
        text="SISTEMA DE PARQUEO",
        font=("Arial",26,"bold")
    )
    titulo.pack(pady=30)
    botonObtener=ctk.CTkButton(
        ventana,
        text="1. Obtener vehículos",
        width=300,
        command=lambda: messagebox.showinfo(
            "Pendiente",
            "Función en desarrollo."
        )
    )
    botonObtener.pack(pady=8)
    botonVer=ctk.CTkButton(
        ventana,
        text="2. Ver estacionamiento",
        width=300,
        command=lambda: messagebox.showinfo(
            "Pendiente",
            "Función en desarrollo."
        )
    )
    botonVer.pack(pady=8)
    botonEstacionar=ctk.CTkButton(
        ventana,
        text="3. Estacionar vehículo",
        width=300,
        command=lambda: messagebox.showinfo(
            "Pendiente",
            "Función en desarrollo."
        )
    )
    botonEstacionar.pack(pady=8)
    botonReportes=ctk.CTkButton(
        ventana,
        text="4. Reportes",
        width=300,
        command=lambda: messagebox.showinfo(
            "Pendiente",
            "Función en desarrollo."
        )
    )
    botonReportes.pack(pady=8)
    botonConfiguracion=ctk.CTkButton(
        ventana,
        text="5. Configuración",
        width=300,
        command=lambda: messagebox.showinfo(
            "Pendiente",
            "Función en desarrollo."
        )
    )
    botonConfiguracion.pack(pady=8)
    botonAcerca=ctk.CTkButton(
        ventana,
        text="6. Acerca de",
        width=300,
        command=lambda: messagebox.showinfo(
            "Pendiente",
            "Función en desarrollo."
        )
    )
    botonAcerca.pack(pady=8)
    botonSalir=ctk.CTkButton(
        ventana,
        text="7. Salir",
        width=300,
        command=ventana.destroy
    )
    botonSalir.pack(pady=20)
    ventana.mainloop()

abrirVentanaPrincipal()
