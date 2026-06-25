#Creado por: Alejandro Sibaja Badilla y Marco Herrera Gómez
#Fecha de creación: 18/06/26
#Ultima modificación:
#Versión de python: 3.14

import pickle
def guardarBD(plistaVehiculos):
    """
    Funcionalidad:
    Guarda la lista de objetos en memoria secundaria.
    Entradas:
    - plistaVehiculos(list): Lista de objetos Estacionamiento.
    Salidas:
    Archivo pickle actualizado.
    """
    archivo=open("vehiculos.pkl","wb")
    pickle.dump(plistaVehiculos,archivo)
    archivo.close()


def cargarBD():
    """
    Funcionalidad:
    Carga la base de datos desde memoria secundaria.
    Entradas:
    Ninguna.
    Salidas:
    Lista de objetos Estacionamiento.
    """
    try:
        archivo=open("vehiculos.pkl","rb")
        listaVehiculos=pickle.load(archivo)
        archivo.close()
        return listaVehiculos
    except:
        return []