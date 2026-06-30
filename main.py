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
    -ventanaPrincipal(objeto):Ventana padre desde donde se invoca.
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

def verEstacionamiento(ventanaPrincipal,entTamano,listaVehiculos):
    """
    Funcionalidad:
    Crea la interfaz grafica asignando colores segun la disponibilidad y enlaza los botones.
    Entradas:
    -ventanaPrincipal(objeto):Ventana padre del sistema.
    -entTamano(entero):Cantidad de espacios totales a dibujar.
    -listaVehiculos(lista):Lista de objetos Estacionamiento.
    Salidas:
    Ventana con la cuadricula de botones y estados de color aplicados.
    """
    ventanaParqueo=ctk.CTkToplevel(ventanaPrincipal)
    ventanaParqueo.title("Ver Estacionamiento")
    ventanaParqueo.geometry("800x600")
    frameParqueo=ctk.CTkScrollableFrame(ventanaParqueo,width=700,height=500)
    frameParqueo.pack(pady=20)
    for i in range(entTamano):
        colorBoton="green"
        for vehiculo in listaVehiculos:
            if vehiculo.estadia[0]=="A"+str(i+1):
                colorBoton="red"
        btnEspacio=ctk.CTkButton(frameParqueo,text="A"+str(i+1),width=100,height=50,fg_color=colorBoton,command=lambda idx=i: observarEspacio(ventanaParqueo,"A"+str(idx+1),listaVehiculos))
        btnEspacio.grid(row=i//5,column=i%5,padx=10,pady=10)
        
def observarEspacio(ventanaPadre,ubicacion,listaVehiculos):
    """
    Funcionalidad:
    Muestra la informacion del vehiculo estacionado o permite registrar uno nuevo si esta libre.
    Entradas:
    -ventanaPadre(objeto):Ventana de donde proviene.
    -ubicacion(entero):Numero de espacio seleccionado.
    -listaVehiculos(lista):Lista de objetos Estacionamiento.
    Salidas:
    Ventana grafica con la informacion del campo.
    """
    ventanaObservar=ctk.CTkToplevel(ventanaPadre)
    ventanaObservar.title("Observar Espacio")
    ventanaObservar.geometry("400x300")
    vehiculoActual=None
    for v in listaVehiculos:
        if v.estadia[0]==ubicacion:
            vehiculoActual=v
    if vehiculoActual!=None:
        lblInfo=ctk.CTkLabel(
            ventanaObservar,
            text=
            "Placa: "+str(vehiculoActual.info[0])+
            "\nMarca: "+obtenerMarca(vehiculoActual.info[1])+
            "\nColor: "+obtenerColor(vehiculoActual.info[2])+
            "\nTipo: "+obtenerTipo(vehiculoActual.info[3])+
            "\nHora de entrada: "+str(vehiculoActual.estadia[1])
        )
        lblInfo.pack(pady=20)
        btnPagar=ctk.CTkButton(ventanaObservar,text="Pagar")
        btnPagar.pack(pady=5)
    else:
        lblInfo=ctk.CTkLabel(
            ventanaObservar,
            text="Ubicación: A"+str(ubicacion)+"\n\nEstado: Disponible"
        )
        lblInfo.pack(pady=20)

        btnEstacionar=ctk.CTkButton(
            ventanaObservar,
            text="Estacionar",
            command=ventanaEstacionarVehiculo
        )
        btnEstacionar.pack(pady=5)
    btnRegresar=ctk.CTkButton(ventanaObservar,text="Regresar",command=ventanaObservar.destroy)
    btnRegresar.pack(pady=5)

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
                text="Marca: "+obtenerMarca(vehiculo.info[1])
            )

            plabelColor.configure(
                text="Color: "+obtenerColor(vehiculo.info[2])
            )

            plabelTipo.configure(
                text="Tipo: "+obtenerTipo(vehiculo.info[3])
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
    confirmacion=messagebox.askyesno(
        "Confirmar estacionamiento",
        "El costo por hora es de CRC"+str(costoHora)+".\n\n¿Desea confirmar el estacionamiento?"
    )
    if not confirmacion:
        return
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

def cierreDiarioBoton():
    datosProcesados,mensaje=cierreDiario()
    if datosProcesados:
        messagebox.showinfo(
            "Información",
            mensaje
        )
    else:
        messagebox.showerror(
            "Error",
            mensaje
        )

def exportarCSVBoton():
    """
    Funcionalidad:
    Llama a la función que exporta el cierre diario a un archivo CSV.
    Entradas:
    Ninguna.
    Salidas:
    Muestra un mensaje indicando el resultado de la operación.
    """
    datosExportados,mensaje=exportarCierreCSV()
    if datosExportados:
        messagebox.showinfo(
            "Información",
            mensaje
        )
    else:
        messagebox.showerror(
            "Error",
            mensaje
        )

def ventanaReportes():
    """
    Funcionalidad:
    Muestra las opciones relacionadas con los reportes.
    Entradas:
    Ninguna.
    Salidas:
    Abre la ventana de reportes.
    """
    ventana=ctk.CTkToplevel()
    ventana.title("Reportes")
    ventana.geometry("450x350")
    titulo=ctk.CTkLabel(
        ventana,
        text="REPORTES",
        font=("Arial",20,"bold")
    )
    titulo.pack(pady=20)
    botonCierreDiario=ctk.CTkButton(
        ventana,
        text="a. Cierre diario y facturación en masa",
        width=320,
        command=cierreDiarioBoton
    )
    botonCierreDiario.pack(pady=8)
    botonTipoPago=ctk.CTkButton(
        ventana,
        text="b. Cierre por tipo de pago",
        width=320,
        command=lambda: messagebox.showinfo(
            "Pendiente",
            "Función correspondiente a E2."
        )
    )
    botonTipoPago.pack(pady=8)
    botonExportarCSV=ctk.CTkButton(
        ventana,
        text="c. Exportar cierre diario a CSV",
        width=320,
        command=exportarCSVBoton
    )
    botonExportarCSV.pack(pady=8)
    botonRegresar=ctk.CTkButton(
        ventana,
        text="Regresar",
        width=320,
        command=ventana.destroy
    )
    botonRegresar.pack(pady=20)

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
        command=ventanaReportes
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
