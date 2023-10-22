import xml.etree.ElementTree as ET
from ListaSimple import ListaSimple
from Fechas import Fecha
import re

class lecturaMensajesxml():
    
    listaFechas = ListaSimple()
    posi = ["bien", "excelente", "genial"]
    nega = ["malo", "molesta", "molesto"]

    def __init__(self,ruta):
        self.archivo = ET.parse(ruta).getroot()
        self.leerMensajes()
        self.comprobar()


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

            
            self.DeterminarSentimientoMensaje(textoSeparado)

            


    def DeterminarSentimientoMensaje(self, mensajeseparado):
        contador = 0
        contadorPositivos = 0
        contadorNegativos = 0

        texto = [x.lower() for x in mensajeseparado]
        print(texto)

        for sentimientopositivo in self.posi:
            for palabra in texto:
                if palabra == sentimientopositivo:
                    contadorPositivos += 1
            
        for sentimientonegativo in self.nega:
            for palabra in texto:
                if palabra == sentimientonegativo:
                    contadorNegativos += 1

        print("Sentimientos Positivos", contadorPositivos)
        print("Sentimientos Negativos", contadorNegativos)

            
        if contadorPositivos > contadorNegativos:
            print("EL TEXTO ES DE SENTIMIENTO POSITIVO")

        elif contadorPositivos < contadorNegativos:
            print("EL TEXTO ES DE SENTIMIENTO NEGATIVO")

        else:
            print("EL TEXTO ES DE SENTIMIENTO NEUTRO")
        print("----------------------------------------\n")



    def comprobar(self):
        fecha = self.listaFechas.getInicio()
        while fecha:
            print("\n----------------------------------")
            print(fecha.getDato().getFecha())
            fecha.getDato().listaHastags.imprimir()
            fecha.getDato().listaUsuarios.imprimir()
            print("----------------------------------\n")
            fecha = fecha.getSiguiente()



lecturaMensajesxml("DocumentosPrueba/Mensajes.xml")
