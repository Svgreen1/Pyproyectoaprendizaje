import mysql.connector
import serial


PuertoSerie = serial.Serial('COM5', 9600)
while True:
	sensores = str(PuertoSerie.readline())[2:-5]  
	valores=[0,0,0,0,0,0]
	dbConnect = {
		'host':'localhost','user':'root','password':'svalverde1',
		'database':'servi'	
			}
	
	def dividir(texto):
		valores[0]=sensores.find('M')
		valores[1]=sensores.find('D')
		valores[2]=sensores.find('H')
		valores[3]=sensores.find('T')
		valores[4]=sensores.find('G')
		valores[5]=len(sensores)

		sensor1=sensores[valores[0]+1:valores[1]]
		sensor2=sensores[valores[1]+1:valores[2]]
		sensor3=sensores[valores[2]+1:valores[3]]
		sensor4=sensores[valores[3]+1:valores[4]]
		sensor5=sensores[valores[4]+1:valores[5]]
		
		sqLInsertar = "insert into variable(media, desviacion, humedad, temperatura, suelohumedad)values(%s,%s,%s,%s,%s)"
		cursor.execute(sqLInsertar,(sensor1, sensor2, sensor3, sensor4, sensor5))
		conexion.commit()
	conexion = mysql.connector.connect(**dbConnect) ##conexion db
	cursor = conexion.cursor() ##crea el cursor
	print('')
	print('valor sensores ({})'.format(sensores))
	print('')
	dividir(sensores)
	print('')


