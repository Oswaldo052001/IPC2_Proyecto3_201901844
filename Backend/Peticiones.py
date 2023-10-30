import xml.etree.ElementTree as ET
from datetime import datetime
from ListaSimple import ListaSimple
from Fechas import Fecha
from AlmacenarDatos import *

class peticiones():

    def __init__(self, tipopeticion, fechaInicio, fechaFin):
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.tipo = tipopeticion
        self.Datos = ListaSimple()
        self.AguardandoDatosFecha_DateBase()
        #consultarHashtags
        #consultarMenciones
        #consultarSentimientos

        if self.tipo == "consultarHashtags":  
            self.peticionHastags()

        elif self.tipo == "consultarMenciones":
            self.peticionMenciones()

        elif self.tipo == "consultarSentimientos":
            self.peticionSentimientos() 
    
    def AguardandoDatosFecha_DateBase(self):
            
        ruta = "DateBase/Fechas.xml"
        archivoFecha = ET.parse(ruta).getroot()

        for fecha in archivoFecha.findall('Fecha'):
            fechaEncontrada = fecha.get('date')
            Hastags = fecha.find('hashtags')
            Usuarios = fecha.find('usuarios')
            Mensajes = fecha.find('mensajes')
            
            tmpFecha = Fecha(fechaEncontrada)   # Creando objeto sistema que hay en el xml
            self.Datos.agregarFinal(tmpFecha)  # Agregando sistema a la lista de sistemas

            for hastag in Hastags.findall('hashtag'):
                self.Datos.getFin().getDato().agregarHastags(hastag.text)

            for usuario in Usuarios.findall('usuario'):
                self.Datos.getFin().getDato().agregarUsuario(usuario.text)

            for mensaje in Mensajes.findall('mensaje'):
                Tipo = mensaje.get('tipo')
                hora = mensaje.get('hora')
                self.Datos.getFin().getDato().agregarMensaje(mensaje.text.strip(),Tipo, hora)


    def peticionHastags(self):
        
        dateFechaInicio =  datetime.strptime(self.fechaInicio, "%d/%m/%Y")
        dateFechaFin =  datetime.strptime(self.fechaFin, "%d/%m/%Y")

        guardar = GuardarPeticionesHashtags(self.fechaInicio, self.fechaFin)
        fechaIngresada = self.Datos.getInicio()

        while fechaIngresada:
            fecha = fechaIngresada.getDato().getFecha()
            dateFecha = datetime.strptime(fecha, "%d/%m/%Y")

            if dateFecha >= dateFechaInicio and dateFecha <= dateFechaFin:
                guardar.agregarFecha(fecha)
                hastag = fechaIngresada.getDato().listaHastags.getInicio()
                while hastag:
                    contador = 0
                    mensaje = fechaIngresada.getDato().listaMensajes.getInicio()
                    while mensaje:
                        contador += self.buscar(hastag.getDato(),mensaje.getDato().getMensaje())
                        mensaje = mensaje.getSiguiente()

                    guardar.AgregarDatos(hastag.getDato(),str(contador))
                    hastag = hastag.getSiguiente()
            fechaIngresada = fechaIngresada.getSiguiente()
        guardar.crearArchivo()


    
    def peticionMenciones(self):
        dateFechaInicio =  datetime.strptime(self.fechaInicio, "%d/%m/%Y")
        dateFechaFin =  datetime.strptime(self.fechaFin, "%d/%m/%Y")

        guardar = GuardarPeticionesMenciones(self.fechaInicio, self.fechaFin)
        fechaIngresada = self.Datos.getInicio()

        while fechaIngresada:
            fecha = fechaIngresada.getDato().getFecha()
            dateFecha = datetime.strptime(fecha, "%d/%m/%Y")

            if dateFecha >= dateFechaInicio and dateFecha <= dateFechaFin:
                guardar.agregarFecha(fecha)
                usuario = fechaIngresada.getDato().listaUsuarios.getInicio()
                while usuario:
                    contador = 0
                    mensaje = fechaIngresada.getDato().listaMensajes.getInicio()
                    while mensaje:
                        contador += self.buscar(usuario.getDato(),mensaje.getDato().getMensaje())
                        mensaje = mensaje.getSiguiente()
                    guardar.AgregarDatos(usuario.getDato(),str(contador))
                    usuario = usuario.getSiguiente()
            fechaIngresada = fechaIngresada.getSiguiente()
        guardar.crearArchivo()



    def peticionSentimientos(self):

        dateFechaInicio =  datetime.strptime(self.fechaInicio, "%d/%m/%Y")
        dateFechaFin =  datetime.strptime(self.fechaFin, "%d/%m/%Y")

        guardar = GuardarPeticionesSentimientos(self.fechaInicio, self.fechaFin)
        fechaIngresada = self.Datos.getInicio()

        while fechaIngresada:
            fecha = fechaIngresada.getDato().getFecha()
            dateFecha = datetime.strptime(fecha, "%d/%m/%Y")

            if dateFecha >= dateFechaInicio and dateFecha <= dateFechaFin:
                contadorPositivos = 0
                contadorNegativos = 0
                contadorNeutro = 0
                guardar.agregarFecha(fecha)
                mensaje = fechaIngresada.getDato().listaMensajes.getInicio()
                while mensaje:
                    
                    if mensaje.getDato().getTipo() == "positivo":
                        contadorPositivos += 1
                    elif mensaje.getDato().getTipo() == "negativo":
                        contadorNegativos += 1
                    else:
                        contadorNeutro += 1   
                    mensaje = mensaje.getSiguiente()
                guardar.AgregarDatos(str(contadorPositivos), str(contadorNegativos), str(contadorNeutro))
            fechaIngresada = fechaIngresada.getSiguiente()
        guardar.crearArchivo()

#--------------------------------------------------------------------------------------------------------------------------

    def buscar(self, palabra, texto):
        texto = texto.replace(",","")
        texto = texto.replace(".","")
        arreglo = texto.split()
        contador = 0
        for valor in arreglo:
            if valor == palabra:
                contador += 1
        return contador
    
    def Existente(self, palabra, arreglo):
        Existe = False
        if palabra in arreglo:
            Existe = True
        return Existe 
        

