#Liberias a utilizar
import xml.etree.ElementTree as ET
import unicodedata
import re

#Archivos Creados
from salida import ResumenMensajes, resumenConfig
from ListaSimple import ListaSimple
from Fechas import Fecha
from AlmacenarDatos import *

class lecturaxml():
    
    def __init__(self,ruta=None):
        self.senti_posi = []
        self.senti_nega = []
        self.senti_posi_rechazados = []
        self.senti_nega_rechazados = []
        self.listaFechas = ListaSimple()

        self.archivo = ET.parse(ruta).getroot()

        self.AguardandoDatosPensamientos_DateBase()
        self.leerDiccionario()
        self.AguardandoDatosFecha_DateBase()
        self.leerMensajes()
        #self.eliminarDatosFechas()
        #self.eliminarDatosSentimientos()
        #self.comprobar()

    def AguardandoDatosPensamientos_DateBase(self):
        rutaPositivos = "Front/DateBase/PalabrasPositivas.xml"
        rutaNegativos = "Front/DateBase/PalabrasNegativas.xml"
        rutaPositivosRechazados = "Front/DateBase/PalabrasPosiRechazadas.xml"
        rutaNegativosRechazados = "Front/DateBase/PalabrasNegaRechazadas.xml"

        archivoPositivos = ET.parse(rutaPositivos).getroot()
        archivoNegativos = ET.parse(rutaNegativos).getroot()
        archivoPositivosRechazados = ET.parse(rutaPositivosRechazados).getroot()
        archivoNegativosRechazados = ET.parse(rutaNegativosRechazados).getroot()


        for palabra in archivoPositivos.findall('palabra'):
            self.senti_posi.append(palabra.text.strip())
    
        for palabra in archivoNegativos.findall('palabra'):
            self.senti_nega.append(palabra.text.strip())

        for palabra in archivoPositivosRechazados.findall('palabra'):
            self.senti_posi_rechazados.append(palabra.text.strip())

        for palabra in archivoNegativosRechazados.findall('palabra'):
            self.senti_nega_rechazados.append(palabra.text.strip())


#----------------------------------------------------FUNCION PARA LEER MENSAJES----------------------------------------------------------------------------------#


    def leerDiccionario(self):
        
        sentimientosPositivos = self.archivo.find('sentimientos_positivos')
        if sentimientosPositivos:
            #Recorriendo el for de sentimientos positivos
            for palabra in sentimientosPositivos.findall('palabra'):
                palabra.text = self.elimina_tildes(palabra.text.lower().strip())
                if len(self.senti_nega) == 0:

                        #Validando si ya esta agregada esa palabra
                        if self.Existente(palabra.text, self.senti_posi) == False:
                            self.senti_posi.append(palabra.text)
                else:
                    if self.repetidoSentimientoPositivo(palabra.text):
                        #Validando si ya esta agregada esa palabra
                        if self.Existente(palabra.text.strip(), self.senti_posi) == False:
                            self.senti_posi.append(palabra.text)
                
    
        sentimientosNegativos = self.archivo.find('sentimientos_negativos')
        #Recoriendo el for de sientimientos negativos
        if sentimientosNegativos:
            for palabra in sentimientosNegativos.findall('palabra'):
                palabra.text = self.elimina_tildes(palabra.text.lower().strip())
                
                if self.repetidoSentimientoNegativo(palabra.text):

                    #Validando si ya esta agregada esa palabra
                    if self.Existente(palabra.text, self.senti_nega) == False:
                        self.senti_nega.append(palabra.text)


        GuardarPalabrasPositivas(self.senti_posi)
        GuardarPalabrasNegativas(self.senti_nega)
        GuardarPalabrasPositivasRechazadas(self.senti_posi_rechazados)
        GuardarPalabrasNegativasRechazadas(self.senti_nega_rechazados)
        ResumenMensajes(len(self.senti_posi),len(self.senti_nega),len(self.senti_posi_rechazados), len(self.senti_nega_rechazados), "resumenConfig")

#----------------------------------------------------FUNCION PARA LEER MENSAJES----------------------------------------------------------------------------------#

    def leerMensajes(self):
        #EXPRESIONES REGULARES
        ER_hastag = r"#.*#"
        ER_usuario = r"@\w*$"
        ER_fecha = r"\b(0[1-9]|[12]\d|3[01])[/](0[1-9]|1[0-2])[/](19\d\d|20\d\d)\b"
        ER_hora = r'^(?:[01]?\d|2[0-3]):[0-5]\d$'


        #ESTE FOR OBTENEMOS TODA LA INFORMACIÓN DE LOS MENSAJES INGRESADOS
        for mensaje in self.archivo.findall('MENSAJE'):
            #OBTENIENDO LA FECHA
            fecha = mensaje.find('FECHA')
            fecha.text = fecha.text.replace(",","")
            fechaSeparada = fecha.text.split()

            #OBTENIENDO EL TEXTO
            texto = mensaje.find('TEXTO')
            textooriginal = texto.text

            texto.text = texto.text.replace(",","")
            texto.text = texto.text.replace(".","")
            textoSeparado = texto.text.split()
            fechaEncontrada = ""
            horaEncontrada = ""

            for fecha in fechaSeparada:
                if re.findall(ER_fecha,fecha):
                    fechaEncontrada = fecha

            for hora in fechaSeparada:
                if re.findall(ER_hora,hora):
                    horaEncontrada = hora
            
            if self.FechaUnica(fechaEncontrada):
                #CRANDO EL OBJETO FECHA
                tmpFecha = Fecha(fechaEncontrada)   # Creando objeto fecha que hay en el xml
                self.listaFechas.agregarFinal(tmpFecha)  # Agregando fecha a la lista de fechas

                #AGREGANDO LOS HASTAGS
                for hastag in textoSeparado:
                    if re.findall(ER_hastag,hastag):
                        self.listaFechas.getFin().getDato().agregarHastags(hastag)
                
                #AGREGANDO LOS USUARIOS
                for user in textoSeparado:
                    if re.findall(ER_usuario,user):
                        self.listaFechas.getFin().getDato().agregarUsuario(user)

                #AGREGANDO LOS MENSAJES
                tipo = self.DeterminarSentimientoMensaje(textoSeparado)
                self.listaFechas.getFin().getDato().agregarMensaje(textooriginal, tipo, horaEncontrada)
            
            else:
                if self.DatoRepetido(textooriginal,horaEncontrada):
                    #AGREGANDO LOS HASTAGS
                    for hastag in textoSeparado:
                        if re.findall(ER_hastag,hastag):
                            self.fechatemporal.getDato().agregarHastags(hastag)
                    
                    #AGREGANDO LOS USUARIOS
                    for user in textoSeparado:
                        if re.findall(ER_usuario,user):
                            self.fechatemporal.getDato().agregarUsuario(user)

                    #AGREGANDO LOS MENSAJES
                    tipo = self.DeterminarSentimientoMensaje(textoSeparado)
                    self.fechatemporal.getDato().agregarMensaje(textooriginal, tipo, horaEncontrada)
                    
        GuardarDatosFecha(self.listaFechas)
        resumenConfig(self.listaFechas)

#-------------------------------------- FUNCIONES PARA COMPROBRAR REPETIDOS MENSAJES -----------------------------------------------
   
    def AguardandoDatosFecha_DateBase(self):
            
        ruta = "DateBase/Fechas.xml"
        archivoFecha = ET.parse(ruta).getroot()


        for fecha in archivoFecha.findall('Fecha'):
            fechaEncontrada = fecha.get('date')
            Hastags = fecha.find('hashtags')
            Usuarios = fecha.find('usuarios')
            Mensajes = fecha.find('mensajes')
            
            tmpFecha = Fecha(fechaEncontrada)   # Creando objeto sistema que hay en el xml
            self.listaFechas.agregarFinal(tmpFecha)  # Agregando sistema a la lista de sistemas

            for hastag in Hastags.findall('hashtag'):
                self.listaFechas.getFin().getDato().agregarHastags(hastag.text)

            for usuario in Usuarios.findall('usuario'):
                self.listaFechas.getFin().getDato().agregarUsuario(usuario.text)

            for mensaje in Mensajes.findall('mensaje'):
                Tipo = mensaje.get('tipo')
                hora = mensaje.get('hora')

                self.listaFechas.getFin().getDato().agregarMensaje(mensaje.text.strip(),Tipo, hora)


    def FechaUnica(self, fechaingresada):
        FechaUnica = True
        self.fechatemporal = None
        fecha = self.listaFechas.getInicio()
        while fecha:
            if fechaingresada == fecha.getDato().getFecha():
                FechaUnica = False
                self.fechatemporal = fecha
            fecha = fecha.getSiguiente()
        return FechaUnica


    def DatoRepetido(self,texto,hora):
        Unico = True
        txt = self.fechatemporal.getDato().listaMensajes.getInicio()
        while txt:
            textotemporal = txt.getDato().getMensaje()
            horatemporal = txt.getDato().getHora()

            if textotemporal.strip() == texto.strip() and horatemporal == hora:
                Unico = False
            txt = txt.getSiguiente()
        return Unico


#----------------------------------------FUNCIONES PARA COMPROBRAR SENTIMIENTOS REPETIDOS--------------------------------------------
    def Existente(self, palabra, arreglo):
        Existe = False
        if palabra in arreglo:
            Existe = True
        return Existe 

    def elimina_tildes(self,cadena):
        s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
        return s


    def repetidoSentimientoPositivo(self, palabra):
        unico = True
        for valor in self.senti_nega:
            if valor.lower() == palabra.lower():
                #Validando si ya esta agregada esa palabra
                if self.Existente(palabra.strip(), self.senti_posi_rechazados) == False:
                    self.senti_posi_rechazados.append(palabra.lower())
                unico = False
        return unico
 
    def repetidoSentimientoNegativo(self, palabra):
        unico = True
        for valor in self.senti_posi:
            if valor.lower() == palabra.lower():
                #Validando si ya esta agregada esa palabra
                if self.Existente(palabra.strip(), self.senti_nega_rechazados) == False:
                    self.senti_nega_rechazados.append(palabra.lower())
                unico = False
        return unico
    
    def DeterminarSentimientoMensaje(self, mensajeseparado):
        contadorPositivos = 0
        contadorNegativos = 0
        tipoSentimiento = ""

        texto = [x.lower() for x in mensajeseparado]
        
        for sentimientopositivo in self.senti_posi:
            for palabra in texto:
                palabra = self.elimina_tildes(palabra)
                if palabra == sentimientopositivo:
                    contadorPositivos += 1
            
        for sentimientonegativo in self.senti_nega:
            for palabra in texto:
                palabra = self.elimina_tildes(palabra)
                if palabra == sentimientonegativo:
                    contadorNegativos += 1
            
        if contadorPositivos > contadorNegativos:
            tipoSentimiento = "positivo"

        elif contadorPositivos < contadorNegativos:
            tipoSentimiento = "negativo"
        else:
            tipoSentimiento = "neutro"
            
        return tipoSentimiento

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

            mesj = fecha.getDato().listaMensajes.getInicio()
            while mesj:
                print(mesj.getDato().getTipo())
                print(mesj.getDato().getMensaje())
                mesj = mesj.getSiguiente()
            fecha = fecha.getSiguiente()


#--------------------------------------------------- CLASE ELIMINAR --------------------------------------------------------------


class Eliminar():
    
    def __init__(self):
        self.eliminarDatosFechas()
        self.eliminarDatosSentimientos()
        self.eliminarConfiguraciones()

    def eliminarDatosFechas(self):
        rutafecha = "Front/DateBase/Fechas.xml"
        archivofechas = ET.parse(rutafecha)
        fechas = archivofechas.getroot()

        for fecha in fechas.findall('Fecha'):
            fechas.remove(fecha)

        ET.indent(fechas, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        archivofechas.write("Front/DateBase/Fechas.xml", encoding='utf-8', xml_declaration=True)


    def eliminarConfiguraciones(self):
        #Eliminando configuracion
        rutafecha = "Front/ArchivosSalidas/resumenConfig.xml"
        archivofechas = ET.parse(rutafecha)
        archivo = archivofechas.getroot()
        palabraposi = archivo.find('PALABRAS_POSITIVAS')
        palabranega = archivo.find('PALABRAS_POSITIVAS_RECHAZADAS')
        palabraposirecha = archivo.find('PALABRAS_NEGATIVAS')
        palabranegarecha = archivo.find('PALABRAS_NEGATIVAS_RECHAZADAS')
        
        if palabraposi != None:
            archivo.remove(palabraposi)

        if palabranega != None:
            archivo.remove(palabranega)
        
        if palabraposirecha != None:
            archivo.remove(palabraposirecha)
        
        if palabranegarecha != None:
            archivo.remove(palabranegarecha)


        #Eliminando confiMensajes
        ruta = "Front/ArchivosSalidas/resumenMensajes.xml"
        archivoresumen = ET.parse(ruta)
        confiMensajes = archivoresumen.getroot()
        
        for tiempo in confiMensajes.findall('TIEMPO'):
            confiMensajes.remove(tiempo)



        ET.indent(archivoresumen, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        archivoresumen.write("Front/ArchivosSalidas/resumenMensajes.xml", encoding='utf-8', xml_declaration=True)
       
        ET.indent(archivo, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        archivofechas.write("Front/ArchivosSalidas/resumenConfig.xml", encoding='utf-8', xml_declaration=True)

    def eliminarDatosSentimientos(self):
        #Obteniendo las rutas de las bases de datos tipo xml para poder eliminar su contenido
        rutaPositivos = "Front/DateBase/PalabrasPositivas.xml"
        rutaNegativos = "Front/DateBase/PalabrasNegativas.xml"
        rutaPositivosRechazados = "Front/DateBase/PalabrasPosiRechazadas.xml"
        rutaNegativosRechazados = "Front/DateBase/PalabrasNegaRechazadas.xml"

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

        archivoPositivos.write("Front/DateBase/PalabrasPositivas.xml", encoding='utf-8', xml_declaration=True)
        archivoNegativos.write("Front/DateBase/PalabrasNegativas.xml", encoding='utf-8', xml_declaration=True)
        archivoPositivosRechazados.write("Front/DateBase/PalabrasPosiRechazadas.xml", encoding='utf-8', xml_declaration=True)
        archivoNegativosRechazados.write("Front/DateBase/PalabrasNegaRechazadas.xml", encoding='utf-8', xml_declaration=True)



#lecturaxml("C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DocumentosPrueba/Diccionario.xml")
#lecturaxml("C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DocumentosPrueba/Diccionario2.xml")
#lecturaxml("DocumentosPrueba/Mensajes.xml")
#lecturaxml("DocumentosPrueba/Mensajes2.xml")
