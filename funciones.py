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
from random import randint
import csv 
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

def facturarEspacio(vehiculo,tipoPago,montoHora,horaSalida,minutoSalida):
    """
    Funcionalidad:
    Calcula el monto a pagar usando metodos estandar y genera el PDF de la factura con QR.
    Entradas:
    -vehiculo(object):Objeto de la clase Estacionamiento a facturar.
    -tipoPago(int):Tipo de pago seleccionado(1:efectivo,2:SINPE,3:tarjeta).
    -montoHora(int):Costo establecido por hora de parqueo.
    -horaSalida(str):Hora en la que el vehiculo abandona el parqueo.
    -minutoSalida(str):Minuto en el que el vehiculo abandona el parqueo.
    Salidas:
    -montoTotal(int):Monto final calculado a cobrar. Archivos PDF y PNG generados.
    """
    horaEntrada=vehiculo.estadia[1].split(":")
    entHEnt=int(horaEntrada[0])
    entMEnt=int(horaEntrada[1])
    entHSal=int(horaSalida)
    entMSal=int(minutoSalida)
    totalHoras=entHSal-entHEnt
    if entMSal>entMEnt:
        totalHoras=totalHoras+1
    if totalHoras<=0:
        totalHoras=1
    montoTotal=totalHoras*montoHora
    vehiculo.estadia[2]=str(entHSal)+":"+str(entMSal)
    vehiculo.pago=(montoTotal,tipoPago)
    textoQr="Placa:"+str(vehiculo.info[0])+"-Marca:"+str(vehiculo.info[1])+"-Tipo:"+str(vehiculo.info[3])+"-Entrada:"+str(vehiculo.estadia[1])
    imgQr=qrcode.make(textoQr)
    nombreQr="qr_"+str(vehiculo.info[0])+".png"
    imgQr.save(nombreQr)
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=12)
    pdf.cell(200,10,txt="Factura Parqueo-Placa:"+str(vehiculo.info[0]),ln=1,align='C')
    pdf.cell(200,10,txt="Monto a pagar:"+str(montoTotal)+" colones",ln=1,align='C')
    pdf.image(nombreQr,x=85,y=40,w=40)
    pdf.output("factura_"+str(vehiculo.info[0])+"_28-06-2026_"+str(entHSal)+":"+str(entMSal)+".pdf")
    return montoTotal

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

def facturarVehiculoAutomatico(pvehiculo):
    """
    Funcionalidad:
    Factura automáticamente un vehículo pendiente durante el cierre diario.
    Entradas:
    - pvehiculo(objeto Estacionamiento)
    Salidas:
    Actualiza la fecha de salida, el monto y el tipo de pago.
    """
    horaSalida=datetime.now().strftime("%d/%m/%Y %H:%M")
    pvehiculo.estadia[2]=horaSalida
    tipoPago=randint(1,3)
    monto=costoHora
    pvehiculo.pago=(monto,tipoPago)

def cierreDiario():
    """
    Funcionalidad:
    Realiza el cierre diario del estacionamiento.
    Entradas:
    N/A
    Salidas:
    Factura todos los vehículos pendientes y actualiza la base de datos.
    """
    vehiculos=cargarBD()
    for vehiculo in vehiculos:
        if vehiculo.estadia[0]!="":
            if vehiculo.estadia[2]=="":
                facturarVehiculoAutomatico(vehiculo)
    datosGuardados=guardarBD(vehiculos)
    if not datosGuardados:
        return False,"No fue posible realizar el cierre diario."
    generarReporteCierreDiario()
    for vehiculo in vehiculos:
        if vehiculo.estadia[2]!="":
            vehiculo.estadia[0]=""
    datosGuardados=guardarBD(vehiculos)
    if not datosGuardados:
        return False,"No fue posible actualizar la base de datos."
    return True,"Cierre diario realizado correctamente."

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

def obtenerTipoPago(ptipoPago):
    """
    Funcionalidad:
    Convierte el código del tipo de pago en su nombre correspondiente.
    Entradas:
    - ptipoPago(int): Código del tipo de pago.
    Salidas:
    Retorna el nombre del tipo de pago.
    """
    if ptipoPago==1:
        return "Efectivo"
    elif ptipoPago==2:
        return "SINPE"
    elif ptipoPago==3:
        return "Tarjeta"
    return ""

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

def generarReporteCierreDiario():
    """
    Funcionalidad:
    Genera el reporte del cierre diario en formato PDF.
    Entradas:
    Ninguna.
    Salidas:
    Guarda el reporte en el disco.
    """
    vehiculos=cargarBD()
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",18)
    pdf.set_text_color(0,0,180)
    pdf.cell(
        0,
        10,
        "CIERRE DIARIO",
        0,
        1,
        "C"
    )
    pdf.set_font("Arial","",12)
    pdf.set_text_color(0,0,0)
    fechaActual=datetime.now().strftime("%d/%m/%Y")
    pdf.cell(
        0,
        10,
        fechaActual,
        0,
        1,
        "C"
    )
    pdf.ln(5)
    pdf.set_font("Arial","B",10)
    pdf.set_fill_color(220,220,220)
    pdf.cell(30,8,"Ubicación",1,0,"C",True)
    pdf.cell(28,8,"Placa",1,0,"C",True)
    pdf.cell(25,8,"Entrada",1,0,"C",True)
    pdf.cell(25,8,"Salida",1,0,"C",True)
    pdf.cell(42,8,"Tipo pago",1,0,"C",True)
    pdf.cell(30,8,"Monto",1,1,"C",True)
    pdf.set_font("Arial","",9)
    totalEfectivo=0
    totalSINPE=0
    totalTarjeta=0
    totalGeneral=0
    for vehiculo in vehiculos:
        if vehiculo.estadia[2]!="":
            ubicacion=vehiculo.estadia[0]
            placa=vehiculo.info[0]
            entrada=vehiculo.estadia[1].split()[1]
            salida=vehiculo.estadia[2].split()[1]
            tipoPago=obtenerTipoPago(vehiculo.pago[1])
            monto=vehiculo.pago[0]
            pdf.cell(30,8,ubicacion,1)
            pdf.cell(28,8,placa,1)
            pdf.cell(25,8,entrada,1)
            pdf.cell(25,8,salida,1)
            pdf.cell(42,8,tipoPago,1)
            pdf.cell(30,8,"CRC "+str(monto),1,1)
            if vehiculo.pago[1]==1:
                totalEfectivo+=monto
            elif vehiculo.pago[1]==2:
                totalSINPE+=monto
            elif vehiculo.pago[1]==3:
                totalTarjeta+=monto
            totalGeneral+=monto
    pdf.ln(10)
    pdf.set_font("Arial","B",12)
    pdf.set_text_color(180,0,0)
    pdf.cell(
        0,
        8,
        "Total Efectivo: CRC "+str(totalEfectivo),
        0,
        1
    )
    pdf.cell(
        0,
        8,
        "Total SINPE: CRC "+str(totalSINPE),
        0,
        1
    )
    pdf.cell(
        0,
        8,
        "Total Tarjeta: CRC "+str(totalTarjeta),
        0,
        1
    )
    pdf.ln(5)
    pdf.set_font("Arial","B",14)
    pdf.set_text_color(0,120,0)
    pdf.cell(
        0,
        10,
        "TOTAL DEL DÍA: CRC "+str(totalGeneral),
        0,
        1
    )
    nombreReporte="cierre_diario_"+fechaActual.replace("/","-")+".pdf"
    pdf.output(nombreReporte)

def exportarCierreCSV():
    """
    Funcionalidad:
    Exporta la información del cierre diario a un archivo CSV.
    Entradas:
    N/A
    Salidas:
    Guarda el archivo CSV y retorna:
    (True,mensaje) si se exportó correctamente.
    (False,mensaje) si ocurrió un error.
    """
    vehiculos=cargarBD()
    try:
        fechaActual=datetime.now().strftime("%d-%m-%Y_%H-%M")
        nombreArchivo="cierre_diario_"+fechaActual+".csv"
        archivo=open(
            nombreArchivo,
            "w",
            newline="",
            encoding="utf-8"
        )
        datosCSV=csv.writer(archivo)
        datosCSV.writerow([
            "Ubicacion",
            "Placa",
            "Hora Entrada",
            "Hora Salida",
            "Tipo Pago",
            "Monto"
        ])
        for vehiculo in vehiculos:
            if vehiculo.estadia[2]!="":
                datosCSV.writerow([
                    vehiculo.estadia[0],
                    vehiculo.info[0],
                    vehiculo.estadia[1],
                    vehiculo.estadia[2],
                    obtenerTipoPago(vehiculo.pago[1]),
                    vehiculo.pago[0]
                ])
        archivo.close()
        return True,"Archivo CSV generado correctamente."
    except:
        return False,"No fue posible generar el archivo CSV."