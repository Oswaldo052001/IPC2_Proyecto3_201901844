import re
import unicodedata
import xml.etree.ElementTree as ET
import xmltodict
import json



''''
pattern = r"\d{3}-\d{3}-\d{4}"
phone_number = input("Introduce tu número de teléfono (en formato 123-456-7890): ")
if re.match(pattern, phone_number):
    
    print("Número de teléfono válido.")
else:
    print("Número de teléfono inválido. Introduce un número en el formato 123-456-7890.")
'''

'''
# Supongamos que tenemos una lista de números de teléfono con diferentes formatos
telefonos = ["(123) 456-7890", "123-456-7890,", "123.456.7890"]
usuario = ["@Maria", "Omar", "California123", "@Oswaldo_123","@13456Olas"]
fechas = ["17/03/2023","10/08/15","50/15/2028","1-5-23"]
horasss = ["10:15","15:30","25:10"]
parrafo = "Bienvenido a USAC @Omar234 @Kritina12_2, estoy muy satisfecho de que todo lo que hayas visto haya sido excelente esperamos que nos vuelvas a visitar y estaremos alegres de volverte a ver, es importante que tu visita a nuestro hotel #NuevaVista# vaya creciendo y sea un excelente lugar de convivencia y sea cool para los jovenes, cualquier enojo o pésimo servicio que haya visto espero que no los hagan saber para ser un mejor luegar con nada mas que agregar me despido de ustedes y espero #VertePronto# #HoteltNuevaVista#."
parrafo = parrafo.replace(",","")
parrafoSeparado = parrafo.split()
# Utilizamos una expresión regular para extraer los números de teléfono
patron = r"\d{3}[-.\)]*\d{3}[-.\)]*\d{4}"
ER_hastag = r"#.*#"
ER_usuario = r"@\w*$"
ER_fecha = r"\b(0[1-9]|[12]\d|3[01])[/](0[1-9]|1[0-2])[/](19\d\d|20\d\d)\b"
Hora = r'^(?:[01]?\d|2[0-3]):[0-5]\d$'
         

patron2 = r"(@)(\w*$)"
numeros = []
valores = []
usuarios =[]
fecha = []
horas = []

fech = " Guatemala, 17/03/2023 07:30 hrs. "
fech = fech.replace(",","")
fechaSeparada = fech.split()


palabra = "Om"

if palabra in usuario:
    print("Existe")
else: 
    print("No existe")

for telefono in telefonos:
    numeros.append(re.findall(patron, telefono))

for hor in horasss:
    if re.findall(Hora,hor):
        horas.append(hor)

for valor in parrafoSeparado:
    if re.findall(ER_hastag,valor):
        valores.append(valor)

for user in parrafoSeparado:
    if re.findall(ER_usuario,user):
        print(user)
        usuarios.append(user)

for fe in fechaSeparada:
    if re.findall(ER_fecha,fe):
        print("entrooo")
        print(fe)
        fecha.append(fe)


print("\n".join(map(str, horas)))

def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s

stringl = "holá"
sin_tildes = elimina_tildes(stringl)

print (sin_tildes)
#print("\n".join(map(str, numeros)))
#print("\n".join(map(str, valores)))


valores = [1,2,3,2,1,5,6,5,5,5]
repetido = []
unico = []
 
for x in valores:
	if x not in unico:
		unico.append(x)
	else:
		if x not in repetido:
			repetido.append(x)

print("\n".join(map(str, unico)))


ruta = 'DateBase/PeticionesHashtags.xml'
archivo = ET.parse(ruta).getroot()
valores = []
valor = dict()
hashtagas = archivo.find('hashtags')
for fecha in hashtagas.findall('fecha'):
    valor = {'fecha': fecha.get('fecha')}
    for hastag in fecha.findall('hashtag'):
        valor[hastag.text] = hastag.get('cantidad') 
    valores.append(valor)


for k in valor.keys():
    print(k)

for x in valores:
    print(x)'''


import aspose.pdf as pdf

# Load the license
license = pdf.License()
license.set_license("Aspose.Total.lic")

# Create Document class object
document = pdf.Document()

# Load input XML file
document.bind_xml("DocumentosPrueba/Diccionario.xml")

# Convert XML to PDF
document.save("XMLtoPDF.pdf")

print("XML to PDF Converted Successfully")