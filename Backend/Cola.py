from ListaSimple import ListaSimple

class Cola(ListaSimple):

    def enconlar(self, dato):
        ListaSimple.agregarFinal(self, dato)

    def desencolar(self):
        ListaSimple.eliminarInicio(self)