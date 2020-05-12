#!/usr/bin/python3
#"Usage: {0} <host> <port>"

import sys
import hashlib
from socket import *
import struct
import base64

def sum16(data):
    if len(data) % 2:
        data = b'\0' + data

    return sum(struct.unpack('!%sH' % (len(data) // 2), data))


def cksum(data):
    sum_as_16b_words  = sum16(data)
    sum_1s_complement = sum16(struct.pack('!L', sum_as_16b_words))
    _1s_complement    = ~sum_1s_complement & 0xffff
    return _1s_complement

def prueba6(mensaje):
	decodificado=mensaje.decode()
	print (decodificado)
	comienzocadena=decodificado.find(":")
	fincadena=decodificado.find("\n",1,)
	identificador=decodificado[comienzocadena+1:fincadena]
	print("El valor del final de la cadena es:")
	print(identificador)
	
	#rfcstring='https://uclm-arco.github.io/ietf-clone/rfc/rfc'+numero+'.txt'


	#no funciona esta prueba




def prueba5(msg):
	decodificado=msg.decode()
	comienzocadena=decodificado.find(":")
	fincadena=decodificado.find("\n",1,)
	identificador=decodificado[comienzocadena+1:fincadena]
	print("El valor del final de la cadena es:")
	print(identificador)
	
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind(('',3053))#puerto usado anteriormente=3011

	nombre=bytes('YAP', 'utf-8')#struct.pack("s",'YAP')	
	tipo=struct.pack(">H",0)
	code=b'\x00'
	checksum=struct.pack(">H",0)#lo inicializamos a cero

	payload=base64.b64encode(bytes(identificador, 'utf-8'))

	cabecera=nombre+tipo+code+checksum
	paquete=cabecera+payload
	suma=cksum(paquete)
	
	checksum=struct.pack(">H",suma)#lo inicializamos a cero
	
	paquete=nombre+tipo+code+checksum+payload

	#para enviar
	sock.sendto(paquete,('node1',7000))
	msg,servidor = sock.recvfrom(4096)
	
	mensaje=base64.b64decode(msg[8:])
		
	prueba6(mensaje)


def prueba4(msg):
	decodificado=msg.decode()
	comienzocadena=decodificado.find("'")
	fincadena=decodificado.find("'",156,)
	identificador=decodificado[comienzocadena+1:fincadena]
	print("El valor del final de la cadena es:")
	print(identificador)
	
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect(('node1', 10001))

	sock.send(identificador.encode('utf-8'))
	msg = sock.recv(4096)
	#print(msg)

	tamano=msg.split(b':',1)
	size=int(tamano[0].decode())
	
	mensaje=tamano[1]
	

	while 1:
		#print("Entro en bucle while")
		resto=size-len(mensaje)
		if(resto>4096):
			mensaje+=sock.recv(4096)
		else:

			mensaje+=sock.recv(resto)
			
			if(resto==0):
				print('Todo recibido')
				break
	print("Salgo del bucle while")			
	print("Resto:")	
	print(resto)	
	print('size:')	
	print(size)	
	print('El menssaje es de largo:')
	print(len(mensaje))
	sha=hashlib.sha1(mensaje)
	print('El SHA es:')
	print(sha.digest())
	sha=sha.digest()
	sock.send(sha)#Hexdigest,.encode('ascii')
	#codigo repetido de otros metodos deberia hacer 
	#un metodo con este codigo
	while 1:
	
		msg = sock.recv(2048)
		#print("Reply of reto 4 is '{0}'".format(msg.decode()))
		if msg.decode().find('hallenge')!=-1:
			break
	
	print(msg.decode())
	#msg = sock.recv(4096)
	prueba5(msg)

def prueba3(msg):
	decodificado=msg.decode()
	fincadena=decodificado.find('\n')
	cadena=msg[5:fincadena]
	print(cadena.decode())
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect(('node1', 5001))
	
	i=0
	j=1
	data=''
	palabra=''
	while 1:
		msg = sock.recv(4096)
		msg = msg.decode()
		data = data+msg
		#print(data)
		data=data.split()
		for x in range(0,len(data)):
			
					
			if data[x].isdigit()==True:
				i=i+int(data[x])
				#print(i)

			if i>1300:
				while data[x-j].isdigit()==True:
					j=j+1
					print(data[x-j])
				palabra=data[x-j]
				print("La palabra es:")
				print(palabra)
				break

		if palabra!='':
			break

	mensaje=palabra+' '+cadena.decode()
	#print("El mensaje es:")
	#print(mensaje)
	sock.send(mensaje.encode('utf-8'))
	
	msg = sock.recv(4096)
	

	#while que limpia el socket de mensajes antiguos hasta
	#que encuentra el reto
	while 1:
	
		msg = sock.recv(2048)
		#print("Reply of reto 3 is '{0}'".format(msg.decode()))
		if msg.decode().find('hallenge')!=-1:
			break
	
	print(msg.decode())

	prueba4(msg)
	
	

def prueba2(msg):
	decodificado=msg.decode()
	fincadena=decodificado.find('\n')
	cadena=msg[5:fincadena]
	print(cadena.decode())
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect(('node1', 4000))
	
	i=0
	data=''
	while 1:
		msg = sock.recv(2048)
		msg = msg.decode()
		data = data+msg
		if "that's" in msg:
			break
		
	data=data.split()
	for x in range(0,len(data)):
		if data[x]=="that's":
			break
		else:
			i=i+1
			

	print(i)
	msg = sock.recv(2048)
	print("Reply is '{0}'".format(msg.decode()))
	
	mensaje=cadena.decode()+' '+str(i)
	print(mensaje)
	sock.send(mensaje.encode('utf-8'))
		
	#while que limpia el socket de mensajes antiguos hasta
	#que encuentra el reto
	while 1:
	
		msg = sock.recv(2048)
		#print("Reply of reto 2 is '{0}'".format(msg.decode()))
		if msg.decode().find('hallenge')!=-1:
			break

	print(msg.decode())
	prueba3(msg)
	
def prueba1(msg):
	
	decodificado=msg.decode()
	fincadena=decodificado.find('\n')
	cadena=msg[:fincadena]#el codigo en binario, eliminar->b''

	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind(('',3011))
	mensaje='3011'+' '+cadena.decode()
	
	sock.sendto(mensaje.encode('utf-8'),('node1',3000))
	
	msg,servidor = sock.recvfrom(1024)
	print(msg.decode())

	prueba2(msg)

def main():
	sock = socket(AF_INET, SOCK_STREAM)

	
	sock.connect(('node1', 2000))
   
	

	msg = sock.recv(2048)

	print("Reply of mainis '{0}'".format(msg.decode()))
	sock.send("david.utrilla2".encode('utf-8'))
	msg = sock.recv(2048)
	print("Reply of main is '{0}'".format(msg.decode()))
	prueba1(msg)
	sock.close()



try:
	main()
except KeyboardInterrupt:
	pass
