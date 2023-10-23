import xml.etree.ElementTree as ET


class Eliminar():
    
    def eliminarDatosFechas(self):
        rutafecha = "DateBase/Fechas.xml"
        archivofechas = ET.parse(rutafecha)
        fechas = archivofechas.getroot()

        for fecha in fechas.findall('Fecha'):
            fechas.remove(fecha)

        ET.indent(fechas, space="\t", level=0)  # Esta linea de codigo ordena la estructura del archivo xml
        archivofechas.write("DateBase/Fechas.xml", encoding='utf-8', xml_declaration=True)

    def eliminarDatosSentimientos(self):
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

