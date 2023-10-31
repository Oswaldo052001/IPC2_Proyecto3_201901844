
#Liberias a utilizar
import xml.etree.ElementTree as ET
from fpdf import FPDF
# save FPDF() class into a 
# variable pdf

class CrearPDFDiccionario():

    def __init__(self):
        self.pdf = FPDF()
        self.AgregarPalabras()
        self.crearArchivo()

    def AgregarPalabras(self):
        # set style and size of font 
        # that you want in the pdf
        self.pdf.set_font("Arial", size = 15)
        self.pdf.add_page()

                
        #Ingresando a los datos del diccionario
        ruta = "Front/DateBase/PalabrasNegativas.xml"
        archivonegativas = ET.parse(ruta).getroot()

        #Ingresando a los datos del diccionario
        ruta = "Front/DateBase/PalabrasPositivas.xml"
        archivoPositivas = ET.parse(ruta).getroot()

        #Ingresando a los datos del diccionario
        ruta = "Front/DateBase/PalabrasPosiRechazadas.xml"
        archivoPosiRechazadas = ET.parse(ruta).getroot()

        #Ingresando a los datos del diccionario
        ruta = "Front/DateBase/PalabrasNegaRechazadas.xml"
        archivoNegaRechazadas = ET.parse(ruta).getroot()

        self.pdf.set_fill_color(70, 130, 180) #COLOR DE FONDO

        self.pdf.set_text_color(255,0,0) #COLOR ROJO
        self.pdf.cell(200, 10, txt = "DICCIONARIO INGRESADO", ln = 1, align = 'C')
        
        self.pdf.set_text_color(255,255,0) #COLOR
        self.pdf.cell(200, 10, txt = "Palabras Positivas", ln = 2, align = 'C')  
        self.pdf.set_text_color(255,250,240)  
        for palabra in archivoPositivas.findall('palabra'):
            self.pdf.cell(75, 8, txt = "", ln = 0, align = 'C')
            self.pdf.cell(50, 8, txt = palabra.text, border= 1, ln = 1, align = 'C', fill=True)

        self.pdf.set_text_color(255,255,0) #COLOR AMARILLO
        self.pdf.cell(200, 10, txt = "Palabras negativas", ln = 2, align = 'C')  
        self.pdf.set_text_color(255,250,240)  
        for palabra in archivonegativas.findall('palabra'):
            self.pdf.cell(75, 8, txt = "", ln = 0, align = 'C')
            self.pdf.cell(50, 8, txt = palabra.text, border= 1, ln = 1, align = 'C', fill = True)

            
        self.pdf.set_text_color(255,255,0) #COLOR AMARILLO
        self.pdf.cell(200, 10, txt = "Palabras positivas rechazadas", ln = 2, align = 'C')  
        self.pdf.set_text_color(255,250,240)  
        for palabra in archivoPosiRechazadas.findall('palabra'):
            self.pdf.cell(75, 8, txt = "", ln = 0, align = 'C')
            self.pdf.cell(50, 8, txt = palabra.text, border= 1, ln = 1, align = 'C', fill=True)

            
        self.pdf.set_text_color(255,255,0) #COLOR AMARILLO
        self.pdf.cell(200, 10, txt = "Palabras negativas rechazadas", ln = 2, align = 'C')  
        self.pdf.set_text_color(255,250,240)  
        for palabra in archivoNegaRechazadas.findall('palabra'):
            self.pdf.cell(75, 8, txt = "", ln = 0, align = 'C')
            self.pdf.cell(50, 8, txt = palabra.text, border= 1, ln = 1, align = 'C', fill=True)
    
    def crearArchivo(self):
        # save the pdf with name .pdf
        self.pdf.output("Front/static/PDF/diccionario.pdf")   


class crearPDFConfig():

    def __init__(self):
        self.pdf = FPDF()
        self.AgregarPalabras()
        self.crearArchivo()

    def AgregarPalabras(self):
        # set style and size of font 
        # that you want in the pdf
        self.pdf.set_font("Arial", size = 12)
        self.pdf.add_page()

                
        #Ingresando a los datos del diccionario
        ruta = "Front/ArchivosSalidas/resumenConfig.xml"
        archivo = ET.parse(ruta).getroot()

        palabraposi = archivo.find('PALABRAS_POSITIVAS')
        palabranega = archivo.find('PALABRAS_POSITIVAS_RECHAZADAS')
        palabraposirecha = archivo.find('PALABRAS_NEGATIVAS')
        palabranegarecha = archivo.find('PALABRAS_NEGATIVAS_RECHAZADAS')
        
        self.pdf.set_text_color(255,0,0) #COLOR ROJO
        self.pdf.cell(200, 10, txt = "RESUMEN CONFIGURACION", ln = 1, align = 'C')

        if palabraposi != None:
            self.pdf.set_text_color(255,255,0) #COLOR AMARILLO
            self.pdf.set_fill_color(47, 79, 79)
            self.pdf.cell(100, 8, txt = "Cantidad de palabras positivas:", border= 1, ln = 0, align = 'C', fill=True)  
            self.pdf.set_text_color(0,0,255)   #COLOR AZUL
            self.pdf.set_fill_color(95, 158, 160)
            self.pdf.cell(0, 8, txt = palabraposi.text, border= 1, ln = 1, align = 'C', fill=True)
        if palabranega != None:
            self.pdf.set_text_color(255,255,0) #COLOR AMARILLO
            self.pdf.set_fill_color(47, 79, 79)
            self.pdf.cell(100, 8, txt = "Cantidad de palabras negativas:", border= 1, ln = 0, align = 'C', fill =True)  
            self.pdf.set_text_color(0,0,255)   #COLOR AZUL
            self.pdf.set_fill_color(95, 158, 160)
            self.pdf.cell(0, 8, txt = palabranega.text, border= 1, ln = 1, align = 'C', fill = True)
        if palabraposirecha != None:
            self.pdf.set_text_color(255,255,0) #COLOR AMARILLO
            self.pdf.set_fill_color(47, 79, 79)
            self.pdf.cell(100, 8, txt = "Cantidad de palabras positivas rechazadas:", border= 1, ln = 0, align = 'C', fill = True)  
            self.pdf.set_text_color(0,0,255)   #COLOR AZUL
            self.pdf.set_fill_color(95, 158, 160)
            self.pdf.cell(0, 8, txt = palabraposirecha.text, border= 1, ln = 1, align = 'C', fill = True)
        if palabranegarecha != None:
            self.pdf.set_text_color(255,255,0) #COLOR AMARILLO
            self.pdf.set_fill_color(47, 79, 79)
            self.pdf.cell(100, 8, txt = "Cantidad de palabras negativas rechazadas:",border= 1, ln = 0, align = 'C', fill= True)  
            self.pdf.set_text_color(0,0,255)   #COLOR AZUL
            self.pdf.set_fill_color(95, 158, 160)
            self.pdf.cell(0, 8, txt = palabranegarecha.text, border= 1, ln = 1, align = 'C', fill= True)


        ruta = "Front/ArchivosSalidas/resumenMensajes.xml"
        archivomensajes = ET.parse(ruta).getroot()

        self.pdf.set_text_color(255,0,0) #COLOR ROJO
        self.pdf.cell(200, 10, txt = "RESUMEN MENSAJES", ln = 1, align = 'C')

        self.pdf.set_text_color(0,0,255)   #COLOR AZUL
        self.pdf.set_fill_color(211, 211, 211)
        self.pdf.cell(40, 8, txt = "Fecha" ,border= 1, ln = 0, align = 'C', fill=True)  
        self.pdf.cell(50, 8, txt = "Mensajes Recibidos", border= 1, ln = 0, align = 'C', fill= True)
        self.pdf.cell(50, 8, txt = "Usuarios Mencionados", border= 1, ln = 0, align = 'C', fill = True)
        self.pdf.cell(50, 8, txt = "Hashtags Incluidos", border= 1, ln = 1, align = 'C', fill = True)

        for tiempo in archivomensajes.findall('TIEMPO'):
            fecha = tiempo.find('FECHA')
            mensajesrecibidos = tiempo.find('MSJ_RECIBIDOS')
            usuariosmencionados = tiempo.find('USR_MENCIONADOS')
            hastagincluidos = tiempo.find('HASH_INCLUIDOS')
            self.pdf.set_fill_color(70, 130, 180)
            self.pdf.set_text_color(255,250,240)   
            self.pdf.cell(40, 8, txt = fecha.text ,border= 1, ln = 0, align = 'C', fill=True)  
            self.pdf.cell(50, 8, txt = mensajesrecibidos.text, border= 1, ln = 0, align = 'C', fill= True)
            self.pdf.cell(50, 8, txt = usuariosmencionados.text, border= 1, ln = 0, align = 'C', fill = True)
            self.pdf.cell(50, 8, txt = hastagincluidos.text, border= 1, ln = 1, align = 'C', fill = True)



    def crearArchivo(self):
        # save the pdf with name .pdf
        self.pdf.output("Front/static/PDF/DiccionarioConfig.pdf")   


CrearPDFDiccionario()