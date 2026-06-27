#Creado por: Alejandro Sibaja Badilla y Marco Herrera Gómez
#Fecha de creación: 18/06/26
#Ultima modificación:
#Versión de python: 3.14
from clases import *
import requests
from archivos import *
vehiculosAPI="https://my.api.mockaroo.com/vehiculos.json?key=7427d5e0"

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