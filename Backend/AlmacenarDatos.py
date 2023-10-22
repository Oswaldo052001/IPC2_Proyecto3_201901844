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



#------------------------------------------------------------------------------------------------------------------------
#               CLASE PARA AGUARDAR LOS HASTAGS Y USUARIOS POR FECHAS
class GuardarDatosFecha():

    root = ET.Element("DatosMensaje")

    def __init__(self, ListaFechas):
        self.listFechas = ListaFechas
        self.AgregarDatos()
        self.crearArchivo()

    def AgregarDatos(self):
        fecha = self.listFechas.getInicio()
        while fecha:
            DatoFecha = ET.SubElement(self.root, "Fecha", date = fecha.getDato().getFecha())
            
            #Insertando las etiquetas con los hashtags ingresados
            hastag = fecha.getDato().listaHastags.getInicio()   
            Hastags = ET.SubElement(DatoFecha, "hashtags", total = str(fecha.getDato().listaHastags.size))         
            while hastag:
                Hast = ET.SubElement(Hastags, "hashtag")
                Hast.text = hastag.getDato()
                hastag = hastag.getSiguiente()

            #Insertando las etiquetas con los usuarios ingresados
            usuario = fecha.getDato().listaUsuarios.getInicio()   
            usuarios = ET.SubElement(DatoFecha, "usuarios", total = str(fecha.getDato().listaUsuarios.size))         
            while usuario:
                Hast = ET.SubElement(usuarios, "usuario")
                Hast.text = usuario.getDato()
                usuario = usuario.getSiguiente()

            fecha = fecha.getSiguiente()

    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        arbol.write("DateBase/Fechas.xml", encoding='utf-8', xml_declaration=True)