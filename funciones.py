#Creado por: Alejandro Sibaja Badilla y Marco Herrera Gómez
#Fecha de creación: 18/06/26
#Ultima modificación:
#Versión de python: 3.14
from clases import *
import requests
from archivos import *
from datetime import datetime
import qrcode
from fpdf import FPDF
vehiculosAPI="https://my.api.mockaroo.com/vehiculos.json?key=7427d5e0"
costoHora=1000

def tamanoDelEstacionamiento(tamano,gracia,monto,electrico):
    """
    Funcionalidad:
    Configura los parametros iniciales calculando los espacios manualmente y a la fuerza bruta.
    Entradas:
    -tamano(str):Cantidad total de espacios digitados.
    -gracia(str):Minutos de gracia permitidos.
    -monto(str):Precio por hora de parqueo en colones.
    -electrico(bool):Indica si el parqueo cuenta con espacio electrico.
    Salidas:
    -listaConfig(list):Lista con la distribucion de espacios calculada.
    """
    esValido=True
    for car in tamano:
        if car<'0' or car>'9':
            esValido=False
    if esValido==True:
        entTamano=int(tamano)
    else:
        entTamano=0
    porcEsp=(entTamano*5)/100
    entEspAux=int(porcEsp)
    if porcEsp>entEspAux:
        entEsp=entEspAux+1
    else:
        entEsp=entEspAux
    if entTamano<40 and entEsp<2:
        entEsp=2
    entElec=0
    if electrico==True:
        entElec=1
    entGen=entTamano-entEsp-entElec
    porcMas=(entGen*5)/100
    entMasAux=int(porcMas)
    if porcMas>entMasAux:
        entMas=entMasAux+1
    else:
        entMas=entMasAux
    entTopeMas=entGen-entMas
    return[entTamano,gracia,monto,entEsp,entElec,entGen,entTopeMas]

def obtenerVehiculos():
    """
    Funcionalidad: Obiene los vehículos desde Mockaroo y construye el diccionario solicitado.
    Entradas: N/A
    Salidas: Diccionario de vehículos
    """
    try:
        respuesta=requests.get(vehiculosAPI)
        if respuesta.status_code!=200:
            return False,{}
        datos=respuesta.json()
        diccionarioVehiculos={}
        for vehiculo in datos:
            placa=vehiculo["placa"]
            diccionarioVehiculos[placa]={
                "id":vehiculo["id"],
                "marca":vehiculo["marca"],
                "color":vehiculo["color"],
                "tipo":vehiculo["tipo"],
                "ubicacion":"",
                "fechaHoraEntrada":"",
                "fechaHoraSalida":"",
                "monto":0,
                "tipoPago":0
            }
        return True,diccionarioVehiculos
    except Exception:
        return False,{}

def crearListaObjetos(diccionarioVehiculos):
    """
    Funcionalidad: Convierte el diccionario de vehículos en la lista oficial de objetos Estacionamiento.
    Entradas: diccionarioVehiculos.
    Salidas: Retorna la lista de objetos.
    """
    objetos=[]
    for placa in diccionarioVehiculos:
        informacion=diccionarioVehiculos[placa]
        info=(
            placa,
            informacion["marca"],
            informacion["color"],
            informacion["tipo"]
        )
        estadia=[
            informacion["ubicacion"],
            informacion["fechaHoraEntrada"],
            informacion["fechaHoraSalida"]
        ]
        pago=(
            informacion["monto"],
            informacion["tipoPago"]
        )
        vehiculo=Estacionamiento(
            str(informacion["id"]),
            info,
            estadia,
            pago
        )
        objetos.append(vehiculo)
    return objetos

def cargarVehiculos():
    """
    Funcionalidad: Obtiene los vehículos desde Mockaroo, crea la lista de objetos
    y la guarda en memoria secundaria.
    Entradas: N/A
    Salidas: True si todo salió correctamente, False si ocurrió un error.
    """
    datosObtenidos,diccionarioVehiculos=obtenerVehiculos()
    if not datosObtenidos:
        return False,{}
    listaObjetos=crearListaObjetos(diccionarioVehiculos)
    datosGuardados=guardarBD(listaObjetos)
    if not datosGuardados:
        return False,{}
    return True, diccionarioVehiculos

def estacionarVehiculo(pplaca, pubicacion):
    """
    Funcionalidad:
    Registra la entrada de un vehículo al estacionamiento.

    Entradas:
    - pplaca(str): Placa del vehículo.
    - pubicacion(str): Ubicación asignada.

    Salidas:
    Retorna:
    (True,mensaje) si el vehículo fue estacionado.
    (False,mensaje) si ocurrió algún error.
    """
    if pubicacion=="":
        return False,"Debe ingresar una ubicación."
    vehiculos=cargarBD()
    for vehiculo in vehiculos:
        if vehiculo.info[0]==pplaca:
            if vehiculo.estadia[0]!="":
                return False, "El vehiculo ya se encuentra estacionado"
            horaEntrada=datetime.now().strftime("%d/%m/%Y %H:%M")
            vehiculo.estadia[0]=pubicacion
            vehiculo.estadia[1]=horaEntrada
            vehiculo.estadia[2]=""
            datosGuardados=guardarBD(vehiculos)
            if not datosGuardados:
                return False, "No fue posible guardar la información."
            textoQR=(pplaca+"-"+obtenerMarca(vehiculo.info[1])+"-"+obtenerTipo(vehiculo.info[3])+"-"+horaEntrada)
            archivoQR=generarQR(textoQR,"qr_"+pplaca+".png")
            generarVoucherPDF(pplaca, obtenerMarca(vehiculo.info[1]), obtenerTipo(vehiculo.info[3]), horaEntrada, archivoQR)
            return True, "Vehículo estacionado correctamente."
    return False, "La placa no se encuentra registrada."

def obtenerMarca(pmarca):
    """
    Funcionalidad:
    Convierte el código numérico de la marca a su nombre.
    Entradas:
    - pmarca(int): Código de la marca.
    Salidas:
    Nombre de la marca.
    """
    marcas=[
        "Toyota",
        "Honda",
        "Hyundai",
        "Nissan",
        "Kia",
        "Suzuki",
        "Mazda",
        "Chevrolet",
        "Ford",
        "Mitsubishi"
    ]
    if pmarca>=1 and pmarca<=10:
        return marcas[pmarca-1]
    return "Desconocida"

def obtenerColor(pcolor):
    """
    Funcionalidad:
    Convierte el código numérico del color a su nombre.
    Entradas:
    - pcolor(int): Código del color.
    Salidas:
    Nombre del color.
    """
    colores=[
        "Blanco",
        "Negro",
        "Gris",
        "Azul",
        "Rojo",
        "Plateado",
        "Verde",
        "Amarillo"
    ]
    if pcolor>=1 and pcolor<=8:
        return colores[pcolor-1]
    return "Desconocido"

def obtenerTipo(ptipo):
    """
    Funcionalidad:
    Convierte el código numérico del tipo de vehículo.
    Entradas:
    - ptipo(int): Código del tipo.
    Salidas:
    Nombre del tipo de vehículo.
    """
    tipos=[
        "Sedán",
        "SUV",
        "Pick-Up",
        "Hatchback"
    ]
    if ptipo>=1 and ptipo<=4:
        return tipos[ptipo-1]
    return "Desconocido"

def generarQR(ptexto,pnombreArchivo):
    """
    Funcionalidad:
    Genera un código QR con la información recibida.
    Entradas:
    - ptexto(str): Información que contendrá el QR.
    - pnombreArchivo(str): Nombre del archivo.
    Salidas:
    Retorna el nombre del archivo generado.
    """
    codigoQR=qrcode.make(ptexto)
    codigoQR.save(pnombreArchivo)
    return pnombreArchivo

def generarVoucherPDF(pplaca, pmarca, ptipo, pfechaHoraEntrada, parchivoQR):
    """
    Funcionalidad:
    Genera el voucher en formato PDF.
    Entradas:
    - pplaca(str)
    - pmarca(str)
    - ptipo(str)
    - pfechaHoraEntrada(str)
    - parchivoQR(str)
    Salidas:
    Guarda el voucher en el disco.
    """
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(
        0,
        10,
        "VOUCHER DE ESTACIONAMIENTO",
        ln=True,
        align="C"
    )
    pdf.ln(10)
    pdf.set_font("Arial","",12)
    pdf.cell(
        0,
        10,
        "Placa: "+pplaca,
        ln=True
    )
    pdf.cell(
        0,
        10,
        "Marca: "+pmarca,
        ln=True
    )
    pdf.cell(
        0,
        10,
        "Tipo: "+ptipo,
        ln=True
    )
    pdf.cell(
        0,
        10,
        "Fecha y hora de entrada: "+pfechaHoraEntrada,
        ln=True
    )
    pdf.ln(10)
    pdf.image(
        parchivoQR,
        x=70,
        w=70
    )
    fechaHora=pfechaHoraEntrada.split()
    fecha=fechaHora[0].replace("/","-")
    hora=fechaHora[1].replace(":","-")
    nombreVoucher="voucher_"+pplaca+"_"+fecha+"_"+hora+".pdf"
    pdf.output(nombreVoucher)