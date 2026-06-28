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
def verEstacionamiento(ventanaPrincipal,entTamano):
    """
    Funcionalidad:
    Crea la interfaz grafica con el grid de espacios del parqueo.
    Entradas:
    -ventanaPrincipal(object):Ventana padre del sistema.
    -entTamano(int):Cantidad de espacios totales a dibujar.
    Salidas:
    Ventana con la cuadricula de botones generada.
    """
    ventanaParqueo=ctk.CTkToplevel(ventanaPrincipal)
    ventanaParqueo.title("Ver Estacionamiento")
    ventanaParqueo.geometry("800x600")
    frameParqueo=ctk.CTkScrollableFrame(ventanaParqueo,width=700,height=500)
    frameParqueo.pack(pady=20)
    for i in range(entTamano):
        btnEspacio=ctk.CTkButton(frameParqueo,text="Espacio "+str(i+1),width=100,height=50,fg_color="green")
        btnEspacio.grid(row=i//5,column=i%5,padx=10,pady=10)

def obtenerVehiculosBoton():
    vehiculosCargados,diccionarioVehiculos=cargarVehiculos()
    if vehiculosCargados:
        print("\n===== DICCIONARIO DE VEHÍCULOS =====\n")
        for placa in diccionarioVehiculos:
            print(placa)
            print(diccionarioVehiculos[placa])
            print("-"*50)
        messagebox.showinfo(
            "Éxito",
            "Vehículos obtenidos correctamente."
        )
    else:
        messagebox.showerror(
            "Error",
            "No fue posible obtener los vehículos."
        )

def buscarVehiculo(pplaca,plistaVehiculos,plabelMarca,plabelColor,plabelTipo):
    """
    Funcionalidad:
    Muestra la información del vehículo seleccionado.
    Entradas:
    - pplaca(str)
    - plistaVehiculos(lista)
    - plabelMarca(CTkLabel)
    - plabelColor(CTkLabel)
    - plabelTipo(CTkLabel)
    Salidas:
    Actualiza los labels de la ventana.
    """
    for vehiculo in plistaVehiculos:
        if vehiculo.info[0]==pplaca:
            plabelMarca.configure(
                text="Marca: "+str(vehiculo.info[1])
            )
            plabelColor.configure(
                text="Color: "+str(vehiculo.info[2])
            )
            plabelTipo.configure(
                text="Tipo: "+str(vehiculo.info[3])
            )
            break

def estacionarVehiculoBoton(pplaca,pubicacion,pventana):
    """
    Funcionalidad:
    Llama a la función de estacionar un vehículo y muestra el resultado.
    Entradas:
    - pplaca(str)
    - pubicacion(str)
    - pventana(CTkToplevel)
    Salidas:
    Muestra un mensaje y cierra la ventana si la operación fue exitosa.
    """
    vehiculoEstacionado,mensaje=estacionarVehiculo(
        pplaca,
        pubicacion
    )
    if vehiculoEstacionado:
        messagebox.showinfo(
            "Información",
            mensaje
        )
        pventana.destroy()
    else:
        messagebox.showerror(
            "Error",
            mensaje
        )

def ventanaEstacionarVehiculo():
    listaVehiculos=cargarBD()
    listaPlacas=[]
    for vehiculo in listaVehiculos:
        listaPlacas.append(vehiculo.info[0])
    ventana=ctk.CTkToplevel()
    ventana.title("Estacionar vehículo")
    ventana.geometry("420x500")
    titulo=ctk.CTkLabel(
        ventana,
        text="ESTACIONAR VEHÍCULO",
        font=("Arial",20,"bold")
    )
    titulo.pack(pady=20)
    ctk.CTkLabel(
        ventana,
        text="Placa:"
    ).pack()
    comboPlaca=ctk.CTkComboBox(
        ventana,
        values=listaPlacas,
        width=220
    )
    comboPlaca.pack(pady=5)
    labelMarca=ctk.CTkLabel(
        ventana,
        text="Marca:"
    )
    labelMarca.pack(pady=5)
    labelColor=ctk.CTkLabel(
        ventana,
        text="Color:"
    )
    labelColor.pack(pady=5)
    labelTipo=ctk.CTkLabel(
        ventana,
        text="Tipo:"
    )
    labelTipo.pack(pady=5)
    botonBuscar=ctk.CTkButton(
        ventana,
        text="Buscar",
        command=lambda: buscarVehiculo(
            comboPlaca.get(),
            listaVehiculos,
            labelMarca,
            labelColor,
            labelTipo
        )
    )
    botonBuscar.pack(pady=10)
    ctk.CTkLabel(
        ventana,
        text="Ubicación:"
    ).pack()
    entryUbicacion=ctk.CTkEntry(
        ventana,
        width=220
    )
    entryUbicacion.pack(pady=5)
    botonEstacionar=ctk.CTkButton(
        ventana,
        text="Estacionar",
        command=lambda: estacionarVehiculoBoton(
            comboPlaca.get(),
            entryUbicacion.get(),
            ventana
        )
    )
    botonEstacionar.pack(pady=20)
    botonRegresar=ctk.CTkButton(
        ventana,
        text="Regresar",
        command=ventana.destroy
    )
    botonRegresar.pack()

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
    botonObtenerVehiculos=ctk.CTkButton(
        ventana,
        text="1. Obtener vehículos",
        width=300,
        command=obtenerVehiculosBoton
    )
    botonObtenerVehiculos.pack(pady=8)
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
        text="2. Estacionar vehículo",
        width=300,
        command=ventanaEstacionarVehiculo
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
