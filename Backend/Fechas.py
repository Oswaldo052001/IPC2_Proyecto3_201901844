from Cola import Cola


class Fecha():

    def __init__(self,date):
        self.fecha = date
        self.listaHastags = Cola()
        self.listaUsuarios = Cola()
        
    def agregarHastags(self,hastag):
        self.listaHastags.enconlar(hastag)

    def agregarUsuario(self, usuario):
        self.listaUsuarios.enconlar(usuario)

    def getFecha(self):
        return self.fecha
    
    def setFecha(self, fecha):
        self.fecha = fecha
    
        


