#Creado por: Alejandro Sibaja Badilla y Marco Herrera Gómez
#Fecha de creación: 18/06/26
#Ultima modificación:
#Versión de python: 3.14
from clases import *
import requests
from archivos import *
vehiculosAPI="https://my.api.mockaroo.com/vehiculos.json?key=7427d5e0"

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
