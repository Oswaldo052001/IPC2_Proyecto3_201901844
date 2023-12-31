import xml.etree.cElementTree as ET

#------------------------------------------------------------------------------------------------------------------------
#                       CLASE PARA AGUARDAR LAS PALABRAS POSITIVAS EN UN XML COMO BASE DE DATOS
class GuardarPalabrasPositivas():

    def __init__(self, valores):
        self.root = ET.Element("PalabrasPositivas")
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
        #arbol.write("DateBase/PalabrasPositivas.xml", encoding='utf-8', xml_declaration=True)
        arbol.write("Front/DateBase/PalabrasPositivas.xml", encoding='utf-8', xml_declaration=True)

#------------------------------------------------------------------------------------------------------------------------
#                       CLASE PARA AGUARDAR LAS PALABRAS NEGATIVAS EN UN XML COMO BASE DE DATOS
class GuardarPalabrasNegativas():

    def __init__(self, valores):
        self.root = ET.Element("PalabrasNegativas")
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
        #arbol.write("DateBase/PalabrasNegativas.xml", encoding='utf-8', xml_declaration=True)
        arbol.write("Front/DateBase/PalabrasNegativas.xml", encoding='utf-8', xml_declaration=True)



#------------------------------------------------------------------------------------------------------------------------
#               CLASE PARA AGUARDAR LAS PALABRAS POSITIVAS RECHAZADAS EN UN XML COMO BASE DE DATOS
class GuardarPalabrasPositivasRechazadas():

    def __init__(self, valores):
        self.root = ET.Element("PalabrasPositivasRechazadas")
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
        #arbol.write("DateBase/PalabrasPosiRechazadas.xml", encoding='utf-8', xml_declaration=True)
        arbol.write("Front/DateBase/PalabrasPosiRechazadas.xml", encoding='utf-8', xml_declaration=True)


#------------------------------------------------------------------------------------------------------------------------
#               CLASE PARA AGUARDAR LAS PALABRAS NEGATIVAS RECHAZADAS EN UN XML COMO BASE DE DATOS
class GuardarPalabrasNegativasRechazadas():

    def __init__(self, valores):
        self.root = ET.Element("PalabrasNegativasRechazadas")
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
        #arbol.write("DateBase/PalabrasNegaRechazadas.xml", encoding='utf-8', xml_declaration=True)
        arbol.write("Front/DateBase/PalabrasNegaRechazadas.xml", encoding='utf-8', xml_declaration=True)




#------------------------------------------------------------------------------------------------------------------------
#               CLASE PARA AGUARDAR LOS HASTAGS Y USUARIOS POR FECHAS
class GuardarDatosFecha():

    def __init__(self, ListaFechas):
        self.root = ET.Element("DatosMensaje")
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

            #Insertando los mensajes en esa fecha
            mesj = fecha.getDato().listaMensajes.getInicio()
            mensajes = ET.SubElement(DatoFecha, "mensajes", total = str(fecha.getDato().listaMensajes.size))
            while mesj:
                mensaje = ET.SubElement(mensajes, "mensaje", tipo = mesj.getDato().getTipo(), hora =  mesj.getDato().getHora() )
                mensaje.text = mesj.getDato().getMensaje().strip()
                mesj = mesj.getSiguiente()

            fecha = fecha.getSiguiente()


    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        #arbol.write("DateBase/Fechas.xml", encoding='utf-8', xml_declaration=True)
        arbol.write("Front/DateBase/Fechas.xml", encoding='utf-8', xml_declaration=True)


#------------------------------------------------------------------------------------------------------------------------
#               CLASE PARA AGUARDAR LAS PALABRAS NEGATIVAS RECHAZADAS EN UN XML COMO BASE DE DATOS
class GuardarPeticionesHashtags():

    def __init__(self, inicio, fin):
        self.root = ET.Element("PeticionesHashtags")
        self.hastags = ET.SubElement(self.root, "hashtags", fechaInicio = inicio, fechaFin = fin)

    def agregarFecha(self, date):
        self.fecha = ET.SubElement(self.hastags, "fecha", fecha = date)

    def AgregarDatos(self, hastag, total):
        hashtag = ET.SubElement(self.fecha, "hashtag", cantidad = total)
        hashtag.text = hastag

    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        #arbol.write("DateBase/PeticionesHashtags.xml", encoding='utf-8', xml_declaration=True)
        arbol.write("Front/DateBase/PeticionesHashtags.xml", encoding='utf-8', xml_declaration=True)


class GuardarPeticionesMenciones():

    def __init__(self, inicio, fin):
        self.root = ET.Element("PeticionesMenciones")
        self.hastags = ET.SubElement(self.root, "usuarios", fechaInicio = inicio, fechaFin = fin)

    def agregarFecha(self, date):
        self.fecha = ET.SubElement(self.hastags, "fecha", fecha = date)

    def AgregarDatos(self, user, total):
        usuario = ET.SubElement(self.fecha, "usuario", cantidad = total)
        usuario.text = user

    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        #arbol.write("DateBase/PeticionesMenciones.xml", encoding='utf-8', xml_declaration=True)
        arbol.write("Front/DateBase/PeticionesMenciones.xml", encoding='utf-8', xml_declaration=True)



class GuardarPeticionesSentimientos():

    def __init__(self, inicio, fin):
        self.root = ET.Element("PeticionesSentimientos")
        self.hastags = ET.SubElement(self.root, "Sentimientos", fechaInicio = inicio, fechaFin = fin)

    def agregarFecha(self, date):
        self.fecha = ET.SubElement(self.hastags, "fecha", fecha = date)

    def AgregarDatos(self, valor1, valor2, valor3):
        positivo = ET.SubElement(self.fecha, "Mensajes_positivos")
        positivo.text = valor1
        negativo = ET.SubElement(self.fecha, "Mensajes_negativos")
        negativo.text = valor2
        neutro = ET.SubElement(self.fecha, "Mensajes_nuetros")
        neutro.text = valor3

    def crearArchivo(self):
        arbol = ET.ElementTree(self.root)
        ET.indent(arbol, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        #arbol.write("DateBase/PeticionesSentimientos.xml", encoding='utf-8', xml_declaration=True)
        arbol.write("Front/DateBase/PeticionesSentimientos.xml", encoding='utf-8', xml_declaration=True)