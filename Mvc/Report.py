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
import numpy as np
import generaPDF

class Reports:	
	def __init__(self):
		self.obj_consulta=database.database()	
		self.obj_pdf=generaPDF.Reporte()

	def add_value_label(self,figura,x_list,y_list):
		for i in range(1, len(x_list)+1):
			
			figura.text(i-1,y_list[i-1]/2,y_list[i-1])
	def generar(self):
		dateI=self.calI.get_date().strftime("%Y-%m-%d")
		dateF=self.calF.get_date().strftime("%Y-%m-%d")
		dni=self.dni.get()		
		rows=self.obj_consulta.mediciones_P(dni,dateI,dateF)
		rows1=self.obj_consulta.mediciones_Count(dni,dateI,dateF)
		Categorias=[]
		pesos=[]
		colores=[]		
		for i in range(len(rows)):
			pesos.append(round(rows[i][0]/1000,2))
			Categorias.append(rows[i][1])
			color = tuple(np.random.choice(range(256), size=3)/256)
			colores.append(color)	
		
	
		fig,ax=plt.subplots(nrows=1,ncols=2,figsize=(11,4))
		#plt.title()
		#GRAFICA PESOS VS CATEGORIA
		ax[0].bar(Categorias,pesos,color=colores)
		self.add_value_label(ax[0],Categorias,pesos)
		ax[0].set_title('Reporte del Peso vs Categorias')
		ax[0].set_xlabel('Categorias')
		ax[0].set_ylabel('Peso en KG')
		#GRAFICA CANTIDAD VS CATEGORIA

		CategoriasCount=[]
		PaltasCount=[]
		
		for i in range(len(rows1)):
			PaltasCount.append(rows1[i][0])
			CategoriasCount.append(rows1[i][1])			
		
		ax[1].bar(CategoriasCount,PaltasCount,color=colores)
		self.add_value_label(ax[1],Categorias,PaltasCount)
		ax[1].set_title('Reporte del Cantidad vs Categorias')
		ax[1].set_xlabel('Categorias')
		ax[1].set_ylabel('Cantidad')
		fig.savefig('grafica.png')
		#inicializar canvas...
		
		self.canvas=FigureCanvasTkAgg(fig,master=self.top2)
		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=3,column=0,columnspan=10)
		#btn_imprimir...
		self.btn_imprimir=tk.Button(self.top2,text="Exportar en PDF")
		self.btn_imprimir['command']=lambda:self.obj_pdf.Reporte_(self.dni.get(),dateI,dateF,pesos,Categorias,self.top2)
		self.btn_imprimir.configure(width = 10, activebackground = "#33B5E5", overrelief="raised",bg="#232928",fg="white",cursor='hand2',font=('',12))
		self.btn_imprimir.grid(row=5,column=3)
		
	def Dibujar_Reporte(self):
		self.top2=tk.Toplevel()
		self.top2.title("Reporte Personal")
		self.top2.iconbitmap('../images/statistic.ico')
		self.top2.geometry("1000x600")
		self.top2.resizable(0,0)
		self.top2.grab_set()
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
		
		
  


