import xml.etree.cElementTree as ET


class ResumenMensajes():

    root = ET.Element("CONFIG_RECIBIDA")
    PalabrasPositivas = ET.SubElement(root, "PALABRAS_POSITIVAS")
    PalabrasPosiRechazadas = ET.SubElement(root, "PALABRAS_POSITIVAS_RECHAZADAS")
    Palabrasnegativas = ET.SubElement(root, "PALABRAS_NEGATIVAS")
    PalabrasNegaRechazadas = ET.SubElement(root, "PALABRAS_NEGATIVAS_RECHAZADAS")

    def __init__(self,posi, nega, posiR, negaR, nombre):
        self.positivas = posi
        self.negativas = nega
        self.posiRechazadas = posiR
        self.negaRechazadas = negaR
        self.nombre = nombre
        self.AgregarConfiguracion()
        self.crearArchivo()

    def AgregarConfiguracion(self):

        self.PalabrasPositivas.text = str(self.positivas)
        self.Palabrasnegativas.text = str(self.negativas)
        self.PalabrasPosiRechazadas.text = str(self.posiRechazadas)
        self.PalabrasNegaRechazadas.text = str(self.negaRechazadas)

    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        arbol.write("ArchivosSalidas/"+self.nombre+".xml", encoding='utf-8', xml_declaration=True)




class resumenConfig():
    def __init__(self, ListaFechas):
        self.root = ET.Element("MENSAJES_RECIBIDOS")
        self.listFechas = ListaFechas
        self.AgregarDatos()
        self.crearArchivo()

    def AgregarDatos(self):
        fecha = self.listFechas.getInicio()
        while fecha:
            Tiempo = ET.SubElement(self.root, "TIEMPO")

            DatoFecha = ET.SubElement(Tiempo, "FECHA")
            DatoFecha.text = fecha.getDato().getFecha()

            DatosMensajes= ET.SubElement(Tiempo, "MSJ_RECIBIDOS")
            DatosMensajes.text = str(fecha.getDato().listaMensajes.size)

            DatosUsuarios= ET.SubElement(Tiempo, "USR_MENCIONADOS")
            DatosUsuarios.text = str(fecha.getDato().listaUsuarios.size)


            DatosHashtags= ET.SubElement(Tiempo, "HASH_INCLUIDOS")
            DatosHashtags.text = str(fecha.getDato().listaHastags.size)

            fecha = fecha.getSiguiente()


    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        arbol.write("ArchivosSalidas/resumenMensajes.xml", encoding='utf-8', xml_declaration=True)

