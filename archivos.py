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
    try:
        archivo=open("vehiculos.pkl","wb")
        pickle.dump(plistaVehiculos,archivo)
        archivo.close()
        return True
    except: return False

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
    
def guardarConfiguracionBD(plistaConfiguracion):
    """
    Funcionalidad:
    Guarda la configuración del estacionamiento en memoria secundaria.
    Entradas:
    - plistaConfiguracion(list): Lista con la configuración.
    Salidas:
    Retorna True si se guardó correctamente y False en caso contrario.
    """
    try:
        archivo=open("configuracion.pkl","wb")
        pickle.dump(plistaConfiguracion,archivo)
        archivo.close()
        return True
    except:
        return False

def cargarConfiguracionBD():
    """
    Funcionalidad:
    Carga la configuración del estacionamiento desde memoria secundaria.
    Entradas:
    Ninguna.
    Salidas:
    Retorna la lista con la configuración almacenada.
    """
    try:
        archivo=open("configuracion.pkl","rb")
        listaConfiguracion=pickle.load(archivo)
        archivo.close()
        return listaConfiguracion
    except:
        return []