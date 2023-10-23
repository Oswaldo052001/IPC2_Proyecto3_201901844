
class mensaje():

    def __init__(self,mensaje, tipo, hora):
        self.mensaje = mensaje
        self.tipo = tipo
        self.hora = hora

    def getMensaje(self):
        return self.mensaje
    
    def setMensaje(self,mensaje):
        self.mensaje = mensaje
        
    def getTipo(self):
        return self.tipo
    
    def setTipo(self, tipo):
        self.tipo = tipo
    
    def getHora(self):
        return self.hora
    
    def setHora(self, hora):
        self.hora = hora