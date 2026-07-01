#Creado por: Alejandro Sibaja Badilla y Marco Herrera Gómez
#Fecha de creación: 18/06/26
#Ultima modificación:
#Versión de python: 3.14

import customtkinter as ctk
from funciones import *
from archivos import *
from clases import *
from tkinter import messagebox
def configurarEstacionamiento(ventanaPrincipal):
    """
    Funcionalidad:
    Muestra la ventana para configurar los parametros iniciales del parqueo.
    Entradas:
    -ventanaPrincipal(object):Ventana padre desde donde se invoca.
    Salidas:
    Ventana grafica de configuracion.
    """
    ventanaConfig=ctk.CTkToplevel(ventanaPrincipal)
    ventanaConfig.title("Configuración")
    ventanaConfig.geometry("400x450")
    lblTamano=ctk.CTkLabel(ventanaConfig,text="Tamaño del estacionamiento:")
    lblTamano.pack(pady=5)
    txtTamano=ctk.CTkEntry(ventanaConfig)
    txtTamano.pack(pady=5)
    lblGracia=ctk.CTkLabel(ventanaConfig,text="Tiempo de gracia(minutos):")
    lblGracia.pack(pady=5)
    txtGracia=ctk.CTkEntry(ventanaConfig)
    txtGracia.pack(pady=5)
    lblMonto=ctk.CTkLabel(ventanaConfig,text="Monto por hora(colones):")
    lblMonto.pack(pady=5)
    txtMonto=ctk.CTkEntry(ventanaConfig)
    txtMonto.pack(pady=5)
    chkElectrico=ctk.CTkCheckBox(ventanaConfig,text="¿Tiene espacio eléctrico?")
    chkElectrico.pack(pady=10)
    btnGuardar=ctk.CTkButton(ventanaConfig,text="Guardar",command=lambda:guardarConfiguracion(txtTamano.get(),txtGracia.get(),txtMonto.get(),chkElectrico.get(),ventanaConfig))
    btnGuardar.pack(pady=10)
    btnRegresar=ctk.CTkButton(ventanaConfig,text="Regresar",command=ventanaConfig.destroy)
    btnRegresar.pack(pady=5)
    
def guardarConfiguracion(tamano,gracia,monto,electrico,ventana):
    """
    Funcionalidad:
    Llama a la lógica matemática, guarda la configuración
    y procesa los datos de la interfaz gráfica.
    Entradas:
    - tamano(str): Cantidad de espacios.
    - gracia(str): Minutos de gracia.
    - monto(str): Precio por hora.
    - electrico(int): Estado del checkbox (1: sí, 0: no).
    - ventana(object): Ventana a destruir.
    Salidas:
    Guarda la configuración y cierra la ventana.
    """
    tieneElectrico=False
    if electrico==1:
        tieneElectrico=True
    listaConfig=tamanoDelEstacionamiento(
        tamano,
        gracia,
        monto,
        tieneElectrico
    )
    datosGuardados=guardarConfiguracionBD(listaConfig)
    if not datosGuardados:
        messagebox.showerror(
            "Error",
            "No fue posible guardar la configuración."
        )
        return
    messagebox.showinfo(
        "Información",
        "Configuración guardada correctamente."
    )
    ventana.destroy()

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

def verEstacionamiento(ventanaPrincipal,listaConfig,listaVehiculos):
    """
    Funcionalidad:
    Crea la interfaz grafica asignando colores segun tipo de espacio y disponibilidad.
    Entradas:
    -ventanaPrincipal(object):Ventana padre del sistema.
    -listaConfig(list):Lista con la configuracion del parqueo(tamano,especiales,electricos).
    -listaVehiculos(list):Lista de objetos Estacionamiento.
    Salidas:
    Ventana con la cuadricula de botones y estados de color aplicados.
    """
    ventanaParqueo=ctk.CTkToplevel(ventanaPrincipal)
    ventanaParqueo.title("Ver Estacionamiento")
    ventanaParqueo.geometry("800x600")
    frameParqueo=ctk.CTkScrollableFrame(ventanaParqueo,width=700,height=500)
    frameParqueo.pack(pady=20)
    entTamano=listaConfig[0]
    entEsp=listaConfig[3]
    entElec=listaConfig[4]
    for i in range(entTamano):
        if i<entEsp:
            colorBoton="blue"
        elif i<(entEsp+entElec):
            colorBoton="yellow"
        else:
            colorBoton="green"
        for vehiculo in listaVehiculos:
            if (vehiculo.estadia[0]=="A"+str(i+1)and vehiculo.estadia[2]==""):
                colorBoton="red"
        ctk.CTkLabel(ventanaParqueo,text="Referencia de colores:",font=("Arial",14,"bold")).pack(pady=(10,5))
        ctk.CTkLabel(ventanaParqueo,text="Azul: Espacios para personas con discapacidad",anchor="w").pack()
        ctk.CTkLabel(ventanaParqueo,text="Amarillo: Espacios para vehículos eléctricos",anchor="w").pack()
        ctk.CTkLabel(ventanaParqueo,text="Verde: Espacios comunes",anchor="w").pack()
        ctk.CTkLabel(ventanaParqueo,text="Rojo: Espacio ocupado",anchor="w").pack()
        btnEspacio=ctk.CTkButton(frameParqueo,text="A"+str(i+1),width=100,height=50,fg_color=colorBoton,command=lambda idx=i: observarEspacio(ventanaParqueo,"A"+str(idx+1),listaVehiculos))
        btnEspacio.grid(row=i//5,column=i%5,padx=10,pady=10)

def verEstacionamientoBoton(pventana):
    listaConfiguracion=cargarConfiguracionBD()
    if listaConfiguracion==[]:
        messagebox.showerror(
            "Error",
            "Primero debe configurar el estacionamiento."
        )
        return
    listaVehiculos=cargarBD()
    verEstacionamiento(
        pventana,
        listaConfiguracion,
        listaVehiculos
    )
        
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
            text="Ubicación: "+str(ubicacion)+"\n\nEstado: Disponible"
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
        text="Cierre diario y facturación en masa",
        width=320,
        command=cierreDiarioBoton
    )
    botonCierreDiario.pack(pady=8)
    botonTipoPago=ctk.CTkButton(
        ventana,
        text="Cierre por tipo de pago",
        width=320,
        command=cierreTipoPagoBoton
    )
    botonTipoPago.pack(pady=8)
    botonExportarCSV=ctk.CTkButton(
        ventana,
        text="Exportar cierre diario a CSV",
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

def cierreTipoPagoBoton():
    """
    Funcionalidad:
    Genera el archivo XML con el cierre agrupado por tipo de pago.
    Entradas:
    Ninguna.
    Salidas:
    Genera el archivo XML y muestra el resultado de la operación.
    """
    listaVehiculos=cargarBD()
    try:
        cierrePorTipoDePago(listaVehiculos)
        messagebox.showinfo(
            "Información",
            "Archivo XML generado correctamente."
        )
    except:
        messagebox.showerror(
            "Error",
            "No fue posible generar el archivo XML."
        )

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
        text="Obtener vehículos",
        width=300,
        command=obtenerVehiculosBoton
    )
    botonObtenerVehiculos.pack(pady=8)
    botonVer=ctk.CTkButton(
        ventana,
        text="Ver estacionamiento",
        width=300,
        command=lambda: verEstacionamientoBoton(ventana)
    )
    botonVer.pack(pady=8)
    botonEstacionar=ctk.CTkButton(
        ventana,
        text="Estacionar vehículo",
        width=300,
        command=ventanaEstacionarVehiculo
    )
    botonEstacionar.pack(pady=8)
    botonReportes=ctk.CTkButton(
        ventana,
        text="Reportes",
        width=300,
        command=ventanaReportes
    )
    botonReportes.pack(pady=8)
    botonConfiguracion=ctk.CTkButton(
        ventana,
        text="Configuración",
        width=300,
        command=lambda: configurarEstacionamiento(
            ventana
        )
    )
    botonConfiguracion.pack(pady=8)
    botonAcerca=ctk.CTkButton(
        ventana,
        text="Acerca de",
        width=300,
        command=lambda: acercaDe(
            ventana
        )
    )
    botonAcerca.pack(pady=8)
    botonSalir=ctk.CTkButton(
        ventana,
        text="Salir",
        width=300,
        command=ventana.destroy
    )
    botonSalir.pack(pady=20)
    ventana.mainloop()

abrirVentanaPrincipal()
