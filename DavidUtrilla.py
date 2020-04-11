#!/usr/bin/python3
#"Usage: {0} <host> <port>"

import sys
from socket import *

def prueba4(msg)

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
				print(palabra)
				break

		if palabra!='':
			break

	mensaje=palabra+' '+cadena.decode()
	print(mensaje)
	sock.send(mensaje.encode('utf-8'))
	msg = sock.recv(2048)
	print("Reply is '{0}'".format(msg.decode()))
	msg = sock.recv(2048)
	print("Reply is '{0}'".format(msg.decode()))
	msg = sock.recv(2048)
	print("Reply is '{0}'".format(msg.decode()))
	
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
		msg = sock.recv(2048)# si no funcionaquitar el mas y los #
		msg = msg.decode()
		data = data+msg
		if "that's" in msg:
			break
		#else:
			#for x in range(0,len(msg)):
				#i=i+1
			#print(i)
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
		

	msg = sock.recv(2048)
	print("Reply is '{0}'".format(msg.decode()))
	prueba3(msg)

def prueba1(msg):
	
	decodificado=msg.decode()
	fincadena=decodificado.find('\n')
	cadena=msg[:fincadena]#el codigo en binario, eliminar->b''

	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind(('',3011))
	mensaje='3011'+' '+cadena.decode()
	
	sock.sendto(mensaje.encode('utf-8'),('node1',3000))
	
	msg,servidor = sock.recvfrom(2048)
	print(msg.decode())

	prueba2(msg)

def main():
	sock = socket(AF_INET, SOCK_STREAM)

	
	sock.connect(('node1', 2000))
   
	#sock.send(data)

	msg = sock.recv(2048)

	print("Reply is '{0}'".format(msg.decode()))
	sock.send("david.utrilla2".encode('utf-8'))
	msg = sock.recv(2048)
	print("Reply is '{0}'".format(msg.decode()))
	prueba1(msg)
	sock.close()

#if len(sys.argv) != 3:
	#print(__doc__.format(__file__))
	#sys.exit(1)

try:
	main()
except KeyboardInterrupt:
	pass
