import xml.etree.cElementTree as ET

#------------------------------------------------------------------------------------------------------------------------
#                       CLASE PARA AGUARDAR LAS PALABRAS POSITIVAS EN UN XML COMO BASE DE DATOS
class GuardarPalabrasPositivas():

    root = ET.Element("PalabrasPositivas")

    def __init__(self, valores):
        self.valores = valores
        self.AgregarDatos()
        self.crearArchivo()

    def AgregarDatos(self):
        for palabra in self.valores:
            PalabraPositiva = ET.SubElement(self.root, "palabra")
            PalabraPositiva.text = palabra

    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        arbol.write("DateBase/PalabrasPositivas.xml", encoding='utf-8', xml_declaration=True)

#------------------------------------------------------------------------------------------------------------------------
#                       CLASE PARA AGUARDAR LAS PALABRAS NEGATIVAS EN UN XML COMO BASE DE DATOS
class GuardarPalabrasNegativas():

    root = ET.Element("PalabrasNegativas")

    def __init__(self, valores):
        self.valores = valores
        self.AgregarDatos()
        self.crearArchivo()

    def AgregarDatos(self):
        for palabra in self.valores:
            PalabraPositiva = ET.SubElement(self.root, "palabra")
            PalabraPositiva.text = palabra

    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        arbol.write("DateBase/PalabrasNegativas.xml", encoding='utf-8', xml_declaration=True)


#------------------------------------------------------------------------------------------------------------------------
#               CLASE PARA AGUARDAR LAS PALABRAS POSITIVAS RECHAZADAS EN UN XML COMO BASE DE DATOS
class GuardarPalabrasPositivasRechazadas():

    root = ET.Element("PalabrasPositivasRechazadas")

    def __init__(self, valores):
        self.valores = valores
        self.AgregarDatos()
        self.crearArchivo()

    def AgregarDatos(self):
        for palabra in self.valores:
            PalabraPositiva = ET.SubElement(self.root, "palabra")
            PalabraPositiva.text = palabra

    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        arbol.write("DateBase/PalabrasPosiRechazadas.xml", encoding='utf-8', xml_declaration=True)


#------------------------------------------------------------------------------------------------------------------------
#               CLASE PARA AGUARDAR LAS PALABRAS NEGATIVAS RECHAZADAS EN UN XML COMO BASE DE DATOS
class GuardarPalabrasNegativasRechazadas():

    root = ET.Element("PalabrasNegativasRechazadas")

    def __init__(self, valores):
        self.valores = valores
        self.AgregarDatos()
        self.crearArchivo()

    def AgregarDatos(self):
        for palabra in self.valores:
            PalabraPositiva = ET.SubElement(self.root, "palabra")
            PalabraPositiva.text = palabra

    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        arbol.write("DateBase/PalabrasNegaRechazadas.xml", encoding='utf-8', xml_declaration=True)