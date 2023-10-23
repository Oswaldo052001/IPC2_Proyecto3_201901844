import xml.etree.ElementTree as ET
from ListaSimple import ListaSimple
import textwrap
from datetime import datetime as dt
from Fechas import Fecha
import re

class lecturaMensajesxml():
    
    listaFechas = ListaSimple()
    posi = ["bien", "excelente", "genial"]
    nega = ["malo", "molesta", "molesto"]

    def __init__(self,ruta):
        self.archivo = ET.parse(ruta).getroot()

        self.AguardandoDatosFecha_DateBase()
        self.leerMensajes()
        #self.comprobar()
        #self.FechaUnica()


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

            

    def DeterminarSentimientoMensaje(self, mensajeseparado):
        contadorPositivos = 0
        contadorNegativos = 0
        tipoSentimiento = ""

        texto = [x.lower() for x in mensajeseparado]

        for sentimientopositivo in self.posi:
            for palabra in texto:
                if palabra == sentimientopositivo:
                    contadorPositivos += 1
            
        for sentimientonegativo in self.nega:
            for palabra in texto:
                if palabra == sentimientonegativo:
                    contadorNegativos += 1
            
        if contadorPositivos > contadorNegativos:
            tipoSentimiento = "positivo"

        elif contadorPositivos < contadorNegativos:
            tipoSentimiento = "negativo"

        else:
            tipoSentimiento = "neutro"

        return tipoSentimiento


    def comprobar(self):
        fecha = self.listaFechas.getInicio()
        while fecha:
            print("\n----------------------------------")
            print(fecha.getDato().getFecha())
            fecha.getDato().listaHastags.imprimir()
            fecha.getDato().listaUsuarios.imprimir()
            print("----------------------------------\n")

            mesj = fecha.getDato().listaMensajes.getInicio()
            while mesj:
                print(mesj.getDato().getTipo(), ":", mesj.getDato().getHora())
                print(mesj.getDato().getMensaje())
                mesj = mesj.getSiguiente()
            fecha = fecha.getSiguiente()

        
lecturaMensajesxml("DocumentosPrueba/Mensajes.xml")
