class Estacionamiento:
    """
    Funcionalidad:
    Almacena la información de un vehículo dentro del sistema.
    Entradas:
    -pid(int): Identificador del vehículo.
    -pinfo(tupla): Información general del vehículo.
    -pestadia(lista): Información de estadía.
    -ppago(tupla): Información de pago.
    Salidas:
    Objeto de tipo Estacionamiento.
    """

    def __init__(self,pid,pinfo,pestadia,ppago):

        self.id=pid
        self.info=pinfo
        self.estadia=pestadia
        self.pago=ppago