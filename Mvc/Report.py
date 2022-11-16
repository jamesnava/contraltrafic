import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import filedialog

class Reports:	
	def __init__(self):
		pass	
		
	def Imprimir(self):
		pass
		
	def Dibujar_Reporte(self):
		nombres=['Jaime','Luis']
		colores=['blue','green']
		tamanio=[25,30]

		self.top2=tk.Toplevel()
		self.top2.title("Reporte Personal")
		self.top2.geometry("700x500")
		etiqueta=tk.Label(self.top2,text='Ingrese su dni: ')
		etiqueta.grid(row=0,column=0)

		self.dni=ttk.Entry(self.top2,width=20)
		self.dni.grid(row=0,column=1)

		fig,ax=plt.subplots(1,2,dpi=80,figsize=(13,4),sharey=True,facecolor='#00f9f844')
		fig.suptitle('Reportes')

		ax[0].bar(nombres,tamanio,color=colores)		
		#inicializar canvas...
		self.canvas=FigureCanvasTkAgg(fig,master=self.top2)
		self.canvas.draw()
		self.canvas.get_tk_widget().grid(row=3,column=0)
		#btn_imprimir...
		self.btn_imprimir=tk.Button(self.top2,text="Imprimir")
		self.btn_imprimir.configure(width = 10,height=4, activebackground = "#33B5E5", overrelief="raised",bg="#232928",fg="white",font=('',12))
		self.btn_imprimir.grid(row=570,column=510)
		self.top2.mainloop()

obj=Reports()
obj.Dibujar_Reporte()


