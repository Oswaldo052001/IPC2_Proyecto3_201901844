import xml.etree.cElementTree as ET


class ArchivoSalida():

    root = ET.Element("CONFIG_RECIBIDA")

    def __init__(self,posi, nega, posiR, negaR, nombre):
        self.positivas = posi
        self.negativas = nega
        self.posiRechazadas = posiR
        self.negaRechazadas = negaR
        self.nombre = nombre

    def AgregarConfiguracion(self):
        PalabrasPositivas = ET.SubElement(self.root, "PALABRAS_POSITIVAS")
        PalabrasPosiRechazadas = ET.SubElement(self.root, "PALABRAS_POSITIVAS_RECHAZADAS")
        Palabrasnegativas = ET.SubElement(self.root, "PALABRAS_NEGATIVAS")
        PalabrasNegaRechazadas = ET.SubElement(self.root, "PALABRAS_NEGATIVAS_RECHAZADAS")

        PalabrasPositivas.text = str(self.positivas)
        Palabrasnegativas.text = str(self.negativas)
        PalabrasPosiRechazadas.text = str(self.posiRechazadas)
        PalabrasNegaRechazadas.text = str(self.negaRechazadas)

    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        arbol.write("ArchivosSalidas/"+self.nombre+".xml", encoding='utf-8', xml_declaration=True)