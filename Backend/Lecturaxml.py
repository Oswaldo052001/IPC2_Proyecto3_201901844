import xml.etree.ElementTree as ET
import unicodedata
from salida import ArchivoSalida
from ListaSimple import ListaSimple
from Fechas import Fecha
import re
from AlmacenarDatos import *

class lecturaxml():
    
    senti_posi = []
    senti_nega = []
    senti_posi_rechazados = []
    senti_nega_rechazados = []
    listaFechas = ListaSimple()

    def __init__(self,ruta):
        self.archivo = ET.parse(ruta).getroot()
        #self.comprobarDatos()
        #self.leerDiccionario()
        self.leerMensajes()
        #self.eliminarDatos()
        #self.comprobar()

    def comprobarDatos(self):
        rutaPositivos = "DateBase/PalabrasPositivas.xml"
        rutaNegativos = "DateBase/PalabrasNegativas.xml"
        rutaPositivosRechazados = "DateBase/PalabrasPosiRechazadas.xml"
        rutaNegativosRechazados = "DateBase/PalabrasNegaRechazadas.xml"

        archivoPositivos = ET.parse(rutaPositivos).getroot()
        archivoNegativos = ET.parse(rutaNegativos).getroot()
        archivoPositivosRechazados = ET.parse(rutaPositivosRechazados).getroot()
        archivoNegativosRechazados = ET.parse(rutaNegativosRechazados).getroot()


        for palabra in archivoPositivos.findall('palabra'):
            self.senti_posi.append(palabra.text)
    
        for palabra in archivoNegativos.findall('palabra'):
            self.senti_nega.append(palabra.text)

        for palabra in archivoPositivosRechazados.findall('palabra'):
            self.senti_posi_rechazados.append(palabra.text)

        for palabra in archivoNegativosRechazados.findall('palabra'):
            self.senti_nega_rechazados.append(palabra.text)


    def eliminarDatos(self):
        #Obteniendo las rutas de las bases de datos tipo xml para poder eliminar su contenido
        rutaPositivos = "DateBase/PalabrasPositivas.xml"
        rutaNegativos = "DateBase/PalabrasNegativas.xml"
        rutaPositivosRechazados = "DateBase/PalabrasPosiRechazadas.xml"
        rutaNegativosRechazados = "DateBase/PalabrasNegaRechazadas.xml"

        archivoPositivos = ET.parse(rutaPositivos)
        palabrasPositivas = archivoPositivos.getroot()

        archivoNegativos = ET.parse(rutaNegativos)
        palabrasNegativas= archivoNegativos.getroot()

        archivoPositivosRechazados = ET.parse(rutaPositivosRechazados)
        palabrasPositivasRechazadas= archivoPositivosRechazados.getroot()

        archivoNegativosRechazados = ET.parse(rutaNegativosRechazados)
        palabrasNegativasRechazadas= archivoNegativosRechazados.getroot()

        #Recorriendo todas las palabras de cada base de datos y luego aliminandolas

        for palabra in palabrasPositivas.findall('palabra'):
            palabrasPositivas.remove(palabra)

        for palabra in palabrasNegativas.findall('palabra'):
            palabrasNegativas.remove(palabra)

        for palabra in palabrasPositivasRechazadas.findall('palabra'):
            palabrasPositivasRechazadas.remove(palabra)

        for palabra in palabrasNegativasRechazadas.findall('palabra'):
            palabrasNegativasRechazadas.remove(palabra)


        # Guardando los datos nuevamente en los archivos
        ET.indent(archivoPositivos, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        ET.indent(archivoNegativos, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        ET.indent(archivoPositivosRechazados, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        ET.indent(archivoNegativosRechazados, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml

        archivoPositivos.write("DateBase/PalabrasPositivas.xml", encoding='utf-8', xml_declaration=True)
        archivoNegativos.write("DateBase/PalabrasNegativas.xml", encoding='utf-8', xml_declaration=True)
        archivoPositivosRechazados.write("DateBase/PalabrasPosiRechazadas.xml", encoding='utf-8', xml_declaration=True)
        archivoNegativosRechazados.write("DateBase/PalabrasNegaRechazadas.xml", encoding='utf-8', xml_declaration=True)



#----------------------------------------------------FUNCION PARA LEER MENSAJES----------------------------------------------------------------------------------#


    def leerDiccionario(self):
        
        sentimientosPositivos = self.archivo.find('sentimientos_positivos')
        if sentimientosPositivos:
            #Recorriendo el for de sentimientos positivos
            for palabra in sentimientosPositivos.findall('palabra'):
                palabra.text = self.elimina_tildes(palabra.text.lower())
                if len(self.senti_nega) == 0:
                        #Validando si ya esta agregada esa palabra
                        if self.Existente(palabra.text, self.senti_posi) == False:
                            palabra.text = self.elimina_tildes(palabra.text.lower())
                            self.senti_posi.append(palabra.text)
                else:
                    if self.repetidoSentimientoPositivo(palabra.text):
                        #Validando si ya esta agregada esa palabra
                        if self.Existente(palabra.text, self.senti_posi) == False:
                            palabra.text = self.elimina_tildes(palabra.text.lower())
                            self.senti_posi.append(palabra.text)
                
    
        sentimientosNegativos = self.archivo.find('sentimientos_negativos')
        #Recoriendo el for de sientimientos negativos
        if sentimientosNegativos:
            for palabra in sentimientosNegativos.findall('palabra'):
                palabra.text = self.elimina_tildes(palabra.text.lower())
                if self.repetidoSentimientoNegativo(palabra.text):
                    #Validando si ya esta agregada esa palabra
                    if self.Existente(palabra.text, self.senti_nega) == False:
                        palabra.text = self.elimina_tildes(palabra.text.lower())
                        self.senti_nega.append(palabra.text)


        GuardarPalabrasPositivas(self.senti_posi)
        GuardarPalabrasNegativas(self.senti_nega)
        GuardarPalabrasPositivasRechazadas(self.senti_posi_rechazados)
        GuardarPalabrasNegativasRechazadas(self.senti_nega_rechazados)
        ArchivoSalida(len(self.senti_posi),len(self.senti_nega),len(self.senti_posi_rechazados), len(self.senti_nega_rechazados), "resumenConfig")

#----------------------------------------------------FUNCION PARA LEER MENSAJES----------------------------------------------------------------------------------#

    def leerMensajes(self):
        #EXPRESIONES REGULARES
        ER_hastag = r"#.*#"
        ER_usuario = r"@\w*$"
        ER_fecha = r"\b(0[1-9]|[12]\d|3[01])[/](0[1-9]|1[0-2])[/](19\d\d|20\d\d)\b"


        #ESTE FOR OBTENEMOS TODA LA INFORMACIÓN DE LOS MENSAJES INGRESADOS
        for mensaje in self.archivo.findall('MENSAJE'):
            #OBTENIENDO LA FECHA
            fecha = mensaje.find('FECHA')
            fecha.text = fecha.text.replace(",","")
            fechaSeparada = fecha.text.split()

            #OBTENIENDO EL TEXTO
            texto = mensaje.find('TEXTO')
            texto.text = texto.text.replace(",","")
            textoSeparado = texto.text.split()

            fechaEncontrada = ""
            for fecha in fechaSeparada:
                if re.findall(ER_fecha,fecha):
                    fechaEncontrada = fecha
                   
            tmpFecha = Fecha(fechaEncontrada)   # Creando objeto sistema que hay en el xml
            self.listaFechas.agregarFinal(tmpFecha)  # Agregando sistema a la lista de sistemas

            for hastag in textoSeparado:
                if re.findall(ER_hastag,hastag):
                    self.listaFechas.getFin().getDato().agregarHastags(hastag)

            for user in textoSeparado:
                if re.findall(ER_usuario,user):
                    self.listaFechas.getFin().getDato().agregarUsuario(user)

        GuardarDatosFecha(self.listaFechas)



#----------------------------------------FUNCIONES PARA COMPROBRAR SENTIMIENTOS REPETIDOS--------------------------------------------
    
    def repetidoSentimientoPositivo(self, palabra):
        unico = True
        for valor in self.senti_nega:
            if valor.lower() == palabra.lower():
                #Validando si ya esta agregada esa palabra
                if self.Existente(palabra, self.senti_posi_rechazados) == False:
                    self.senti_posi_rechazados.append(palabra.lower())
                unico = False
        return unico
 
    def repetidoSentimientoNegativo(self, palabra):
        unico = True
        for valor in self.senti_posi:
            if valor.lower() == palabra.lower():
                #Validando si ya esta agregada esa palabra
                if self.Existente(palabra, self.senti_nega_rechazados) == False:
                    self.senti_nega_rechazados.append(palabra.lower())
                unico = False
        return unico
    
    def elimina_tildes(self,cadena):
        s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
        return s


#-----------------------------------------------  FUNCIONES PARA COMPROBRAR --------------------------------------------------------
    def comprobar1(self):
        print("\nSENTIMIENTOS POSITIVOS")
        print("\n".join(map(str, self.senti_posi)))

        print("\nSENTIMIENTOS NEGATIVOS")
        print("\n".join(map(str, self.senti_nega)))
        
        print("\nSENTIMIENTOS POSITIVOS RECHAZADOS")
        print("\n".join(map(str, self.senti_posi_rechazados)))

        print("\nSENTIMIENTOS NEGATIVOS RECHAZADOS")
        print("\n".join(map(str, self.senti_nega_rechazados)))


    def comprobar2(self):
        fecha = self.listaFechas.getInicio()
        while fecha:
            print("\n----------------------------------")
            print(fecha.getDato().getFecha())
            fecha.getDato().listaHastags.imprimir()
            fecha.getDato().listaUsuarios.imprimir()
            print("----------------------------------\n")
            fecha = fecha.getSiguiente()



lecturaxml("DocumentosPrueba/Mensajes.xml")
#lecturaDicionarioxml("C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DocumentosPrueba/Diccionario.xml")
#lecturaDicionarioxml("C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DocumentosPrueba/Diccionario2.xml")

