#Creado por: Alejandro Sibaja Badilla y Marco Herrera Gómez
#Fecha de creación: 18/06/26
#Ultima modificación:
#Versión de python: 3.14
from clases import *
import requests
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
