#!/usr/bin/python3
#"Usage: {0} <host> <port>"

import sys

from socket import *

def prueba4(msg):
	decodificado=msg.decode()
	comienzocadena=decodificado.find("'")
	fincadena=decodificado.find("'",156,)
	identificador=decodificado[comienzocadena+1:fincadena]
	print("El valor del final de la cadena es:")
	print(identificador)
	
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect(('node1', 10001))

	socket.send(identificador.encode('utf-8'))
	msg = sock.recv(4096)
	print(msg)
	print(msg.decode())



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
		print(data)
		data=data.split()
		for x in range(0,len(data)):
			
					
			if data[x].isdigit()==True:
				i=i+int(data[x])
				print(i)

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
	print("El mensaje es:")
	print(mensaje)
	sock.send(mensaje.encode('utf-8'))
	
	msg = sock.recv(4096)
	print("Reply is '{0}'".format(msg.decode()))

	#while que limpia el socket de mensajes antiguos hasta
	#que encuentra el reto
	while 1:
	
		msg = sock.recv(2048)
		print("Reply is '{0}'".format(msg.decode()))
		if msg.decode().find('hallenge')!=-1:
			break
	
	
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
		print("Reply is '{0}'".format(msg.decode()))
		if msg.decode().find('hallenge')!=-1:
			break


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

	print("Reply is '{0}'".format(msg.decode()))
	sock.send("david.utrilla2".encode('utf-8'))
	msg = sock.recv(2048)
	print("Reply is '{0}'".format(msg.decode()))
	prueba1(msg)
	sock.close()



try:
	main()
except KeyboardInterrupt:
	pass
