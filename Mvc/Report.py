import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import filedialog
from tkcalendar import DateEntry
import database

class Reports:	
	def __init__(self):
		self.obj_consulta=database.database()	
		
	def generar(self):
		dateI=self.calI.get_date().strftime("%Y-%m-%d")
		dateF=self.calF.get_date().strftime("%Y-%m-%d")
		dni=self.dni.get()		
		rows=self.obj_consulta.mediciones_P(dni,dateI,dateF)
		Categorias=['A','B','C']
		PesoA=0
		PesoB=0
		PesoC=0
		for i in range(len(rows)):
			if rows[i][5]=='A':
				PesoA=PesoA+rows[i][3]
			elif rows[i][5]=='B':
				PesoB=PesoB+rows[i][3]
			else:
				PesoC=PesoC+rows[i][3]

		pesos=[PesoA,PesoB,PesoC]
		colores=['blue','green','red']
	
		fig,ax=plt.subplots(1,2,dpi=80,figsize=(13,4),sharey=True,facecolor='#00f9f844')
		ax[0].bar(Categorias,pesos,color=colores)		
		#inicializar canvas...
		self.canvas=FigureCanvasTkAgg(fig,master=self.top2)
		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=3,column=0,columnspan=10)
		#btn_imprimir...
		self.btn_imprimir=tk.Button(self.top2,text="Imprimir")
		self.btn_imprimir.configure(width = 10,height=4, activebackground = "#33B5E5", overrelief="raised",bg="#232928",fg="white",font=('',12))
		self.btn_imprimir.grid(row=570,column=510)
		
	def Dibujar_Reporte(self):
		self.top2=tk.Toplevel()
		self.top2.title("Reporte Personal")
		self.top2.geometry("1000x500")
		etiqueta=tk.Label(self.top2,text='Ingrese su dni: ')
		etiqueta.grid(row=0,column=0)
		self.dni=ttk.Entry(self.top2,width=20)
		self.dni.grid(row=0,column=1)

		etiqueta=tk.Label(self.top2,text='Desde: ')
		etiqueta.grid(row=0,column=2)
		self.calI=DateEntry(self.top2,width=16,background="magenta3",foreground="white",bd=2)
		self.calI.grid(row=0,column=3,pady=10)

		etiqueta=tk.Label(self.top2,text='Hasta: ')
		etiqueta.grid(row=0,column=4)
		self.calF=DateEntry(self.top2,width=16,background="magenta3",foreground="white",bd=2)
		self.calF.grid(row=0,column=5)


		boton_Generar=tk.Button(self.top2,width=20,text='Generar')
		boton_Generar['command']=self.generar
		boton_Generar.grid(row=1,column=3,pady=10)
		
		
  


