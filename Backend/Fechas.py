from Cola import Cola
from Mensaje import mensaje
from ListaSimple import ListaSimple


class Fecha():

    def __init__(self,date):
        self.fecha = date
        self.listaHastags = Cola()
        self.listaUsuarios = Cola()
        self.listaMensajes = ListaSimple()
        
    def agregarHastags(self,hastag):
        self.listaHastags.enconlar(hastag)

    def agregarUsuario(self, usuario):
        self.listaUsuarios.enconlar(usuario)

    def agregarMensaje(self, msj, tipo, hora):
        tmpMensaje = mensaje(msj,tipo, hora)   # Creando objeto sistema que hay en el xml
        self.listaMensajes.agregarFinal(tmpMensaje)  # Agregando sistema a la lista de sistemas

    def getFecha(self):
        return self.fecha
    
    def setFecha(self, fecha):
        self.fecha = fecha
    
        


