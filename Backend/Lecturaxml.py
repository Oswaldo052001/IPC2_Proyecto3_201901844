import xml.etree.ElementTree as ET
import unicodedata
from salida import ArchivoSalida
from ListaSimple import ListaSimple
from Fechas import Fecha
from EliminarDatos import Eliminar
import re
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
        rutaPositivos = "DateBase/PalabrasPositivas.xml"
        rutaNegativos = "DateBase/PalabrasNegativas.xml"
        rutaPositivosRechazados = "DateBase/PalabrasPosiRechazadas.xml"
        rutaNegativosRechazados = "DateBase/PalabrasNegaRechazadas.xml"

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
        ER_hora = r'^(?:[01]?\d|2[0-3]):[0-5]\d$'


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
                self.listaFechas.getFin().getDato().agregarMensaje(texto.text, tipo, horaEncontrada)
            
            else:
                if self.DatoRepetido(texto.text,horaEncontrada):
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
                    self.fechatemporal.getDato().agregarMensaje(texto.text, tipo, horaEncontrada)
                else:
                    print("SE REPITIO")
                    
        GuardarDatosFecha(self.listaFechas)

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




#lecturaDicionarioxml("C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DocumentosPrueba/Diccionario.xml")
#lecturaDicionarioxml("C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DocumentosPrueba/Diccionario2.xml")
#lecturaxml("DocumentosPrueba/Mensajes.xml")
#lecturaxml("DocumentosPrueba/Mensajes2.xml")
