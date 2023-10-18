import xml.etree.ElementTree as ET
from salida import ArchivoSalida

class lecturaxml():
    
    senti_posi = []
    senti_nega = []
    senti_posi_rechazados = []
    senti_nega_rechazados = []

    def __init__(self,ruta):
        self.archivo = ET.parse(ruta).getroot()
        self.leerDiccionario()
        self.leerMensajes()
        #self.comprobar()
    
    def leerDiccionario(self):
        sentimientosPositivos = self.archivo.find('sentimientos_positivos')

        if sentimientosPositivos:
            #Recorriendo el for de sentimientos positivos
            for palabra in sentimientosPositivos.findall('palabra'):
                if len(self.senti_nega) == 0:
                        self.senti_posi.append(palabra.text)
                else:
                    if self.repetidoSentimientoPositivo(palabra.text):
                        self.senti_nega.append(palabra.text)

        
        sentimientosNegativos = self.archivo.find('sentimientos_negativos')
        #Recoriendo el for de sientimientos negativos
        if sentimientosNegativos:
            for palabra in sentimientosNegativos.findall('palabra'):
                if self.repetidoSentimientoNegativo(palabra.text):
                    self.senti_nega.append(palabra.text)


        archivo = ArchivoSalida(len(self.senti_posi),len(self.senti_nega),len(self.senti_posi_rechazados), len(self.senti_nega_rechazados), "resumenConfig")
        archivo.AgregarConfiguracion()
        archivo.crearArchivo()

    
    def leerMensajes(self):
        for mensaje in self.archivo.findall('MENSAJE'):
            fecha = mensaje.find('FECHA')
            texto = mensaje.find('TEXTO')
            print(fecha.text)
            print(texto.text)

        
    
    def repetidoSentimientoNegativo(self, palabra):
        unico = True
        for valor in self.senti_posi:
            if valor.lower() == palabra.lower():
                self.senti_nega_rechazados.append(palabra)
                unico = False
        return unico
    
    def repetidoSentimientoPositivo(self, palabra):
        unico = True
        for valor in self.senti_nega:
            if valor.lower() == palabra.lower():
                self.senti_posi_rechazados.append(palabra)
                unico = False
        return unico


    def comprobar(self):
        print("\nSENTIMIENTOS POSITIVOS")
        print("\n".join(map(str, self.senti_posi)))

        print("\nSENTIMIENTOS NEGATIVOS")
        print("\n".join(map(str, self.senti_nega)))
        
        print("\nSENTIMIENTOS POSITIVOS RECHAZADOS")
        print("\n".join(map(str, self.senti_posi_rechazados)))

        print("\nSENTIMIENTOS NEGATIVOS RECHAZADOS")
        print("\n".join(map(str, self.senti_nega_rechazados)))
        
prueba = lecturaxml("C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DocumentosPrueba/Diccionario.xml")
prueba2 = lecturaxml("C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DocumentosPrueba/Mensajes.xml")

