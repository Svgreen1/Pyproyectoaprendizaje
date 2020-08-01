import mysql.connector
import serial
import mysql.connector
import serial
import pandas as pd
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox   ##libreria ventanas emergentes
from tkinter import filedialog  
import datetime
import numpy as np
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from matplotlib import pyplot
import sqlalchemy
from sqlalchemy import create_engine
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
	print('')          ##crear los ejecutables.
	engine= sqlalchemy.create_engine("mysql+pymysql://root:svalverde1@localhost:3306/servi")  #/credenciales de ingreso
	df=pd.read_sql_table("variable", engine)
	tabla = df[["media", "humedad", "temperatura", "fechahora"]]
	tX=tabla.get("fechahora") #.astype(str)
	aY=tabla.get("temperatura")
	bY=tabla.get("humedad")
	cY=tabla.get("media")
	class raiz(Tk):
		def __init__(self):     #crear objetos para raiz
			super(raiz, self).__init__()
			self.title("Monitor de variables")
			self.minsize(1200, 670)
			self.matplotCanvas()
			self.iconbitmap("icono1.ico")         
			barramenu=Menu(self)
			self.config(menu=barramenu)
			self.config(bd=25) ##borde
			self.config(relief="groove")
			self.config(bg="black")
			ayudamenu=Menu(barramenu, tearoff=0)
			ayudamenu.add_command(label="Acerca de...", command=emergente)
			barramenu.add_cascade(label="Ayuda", menu=ayudamenu)
			root = raiz()
			root.mainloop()


		def matplotCanvas(self):
			#primer grafico................
			f = Figure(figsize=(11, 7), dpi=80) #pulgadas, Dots per inches dpi
			a = f.add_subplot(311)
			a.plot(tX,aY, color="yellow")
			a.grid(True)  
			a.set_ylabel("°C Temperatura")
			#toolbar=NavigationToolbar2Tk(a,self)
			canvas = FigureCanvasTkAgg(f, self)
			canvas.draw()
			##segundo<<<<<<<<<<<<<<<<<<<<<<<<<<<<
			g = Figure(figsize=(11, 7), dpi=100)
			b = f.add_subplot(312)
			b.plot(tX, bY, color="green")
			b.grid(True)
			b.set_ylabel("% Humedad relativa")
			canvas2 = FigureCanvasTkAgg(g, self)
			canvas2.draw()
			#tercero<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
			h = Figure(figsize=(11, 7), dpi=100)
			c = f.add_subplot(313)
			c.plot(tX, cY, color="red")
			c.grid(True)
			c.set_xlabel("Tiempo")
			c.set_ylabel("% humedad de suelo")
			canvas3 = FigureCanvasTkAgg(h, self)
			canvas3.draw()
			canvas.get_tk_widget().pack(side=TOP, fill=X, expand=True)
			toolbar = NavigationToolbar2Tk(canvas, self).pack(side=LEFT)

	def emergente():
		messagebox.showinfo("Agradecimientos", "Agradecimientos a la Uniajc y la honorable profesora Erika Sarria Navarro")
	root = raiz()
	root.mainloop()
