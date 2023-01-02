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
from tkdocviewer import *
import os
from tkinter.filedialog import askdirectory
import shutil

class Reports:	
	def __init__(self):
		self.obj_consulta=database.database()	
		self.obj_pdf=generaPDF.Reporte()

	def add_value_label(self,figura,x_list,y_list):
		for i in range(1, len(x_list)+1):
			
			figura.text(i-1,y_list[i-1]/2,y_list[i-1])
	def generar(self):		
		#self.dateI=self.calI.get_date().strftime("%Y")+"-"+str(int(self.calI.get_date().strftime("%m")))+"-"+str(int(self.calI.get_date().strftime("%d")))
		#self.dateF=self.calF.get_date().strftime("%Y")+"-"+str(int(self.calF.get_date().strftime("%m")))+"-"+str(int(self.calF.get_date().strftime("%d")))
		self.dateI=self.calI.get_date()
		self.dateF=self.calF.get_date()
		#print(dateI)
		dni=self.dni.get()		
		rows=self.obj_consulta.mediciones_P(dni,self.dateI,self.dateF)
		rows1=self.obj_consulta.mediciones_Count(dni,self.dateI,self.dateF)
		self.Categorias=[]
		self.pesos=[]
		colores=[]		
		for i in range(len(rows)):
			self.pesos.append(round(rows[i][0]/1000,2))
			self.Categorias.append(rows[i][1])
			color = tuple(np.random.choice(range(256), size=3)/256)
			colores.append(color)	
		
	
		fig,ax=plt.subplots(nrows=1,ncols=2,figsize=(11,4))
		#plt.title()
		#GRAFICA PESOS VS CATEGORIA
		ax[0].bar(self.Categorias,self.pesos,color=colores)
		self.add_value_label(ax[0],self.Categorias,self.pesos)
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
		self.add_value_label(ax[1],self.Categorias,PaltasCount)
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
		self.btn_imprimir['command']=self.pdfV
		#self.btn_imprimir['command']=self.viewPDF
		self.btn_imprimir.configure(width = 10, activebackground = "#33B5E5", overrelief="raised",bg="#232928",fg="white",cursor='hand2',font=('',12))
		self.btn_imprimir.grid(row=5,column=3)
		
	def Dibujar_Reporte(self):
		self.top2=tk.Toplevel()
		self.top2.title("Reporte General de la clasificacion de la palta")
		self.top2.iconbitmap('images/statistic.ico')
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


		boton_Generar=tk.Button(self.top2,width=20,text='Generar',cursor='hand2',background="deepskyblue")
		boton_Generar['command']=self.generar
		boton_Generar.grid(row=1,column=3,pady=10)

	def pdfV(self):
		try:
			self.obj_pdf.Reporte_(self.dni.get(),self.dateI,self.dateF,self.pesos,self.Categorias)
			self.viewPDF()
			self.top2.destroy()
		except Exception as e:
			messagebox.showerror('Alerta',f'No pudo Generarse debido al siguiente error {e}')
		
	def viewPDF(self):
		self.ventana_pdf=tk.Toplevel()
		self.ventana_pdf.geometry('800x600')
		#creando menu
		menubar=tk.Menu(self.ventana_pdf)
		self.ventana_pdf.config(menu=menubar)
		archivomenu=tk.Menu(menubar,tearoff=0)
		archivomenu.add_command(label='Imprimir',command=self.printPDF)
		archivomenu.add_command(label='Exportar',command=self.exportarPDF)
		menubar.add_cascade(label='Archivo',menu=archivomenu)
		self.ventana_pdf.resizable(0,0)
		self.ventana_pdf.grab_set()		
		self.ventana_pdf.title('Vista General de Reporte')
		v = DocViewer(self.ventana_pdf)
		v.pack(side = "top", expand = 1, fill = "both")
		# Display some document
		v.display_file("Reporte.pdf")
	def printPDF(self):
		os.startfile('Reporte.pdf','print')
	def exportarPDF(self):
		try:
			address= askdirectory(initialdir=r'D:\\',title='Seleccione Ubicancion para exportar')
			shutil.copy('Reporte.pdf',address)
			messagebox.showinfo('Notificacion','Se exportó correctamente!!')
			self.ventana_pdf.destroy()
		except Exception as e:
			messagebox.showerror('Error',f'error {e}')
		
		
		
  


