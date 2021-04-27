import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter.messagebox as MsgI
from tkinter import filedialog

class Reports:
	"""docstring for Reports"""
	ventana=None
	top2=None
	btn_imprimir=None
	canvas=None
	direccion=None
	figure=None
	tiempo=0
	moto=0
	camion=0
	auto=0
	
	def __init__(self,ventana,moto,camion,auto,tiempo):
		self.moto=int(moto)
		self.camion=int(camion)
		self.auto=int(auto)
		self.tiempo=int(tiempo)
		self.ventana=ventana
		self.top2=tk.Toplevel(self.ventana,bg="green",relief="groove")
		self.top2.title("Reportes")
		self.top2.geometry("1146x570+149+65")
		self.top2.overrideredirect(1)
		self.top2.wm_attributes("-topmost",1)
		#inicializar canvas...
		self.canvas=tk.Canvas(self.top2,width=1132,height=490,bg="blue")
		self.canvas.place(x=5,y=5)
		#btn_imprimir...
		self.btn_imprimir=tk.Button(self.top2,text="Imprimir")
		self.btn_imprimir.configure(command=self.Imprimir,width = 10,height=4, activebackground = "#33B5E5", overrelief="raised",bg="#232928",fg="white",font=('',12))
		self.btn_imprimir.place(x=570,y=510)

		self.ventana.wm_attributes("-disabled",1)
		
		self.Redibujar()
	def Imprimir(self):
		self.ventana.wm_attributes("-disabled",0)
		self.top2.destroy()
		address=filedialog.askdirectory()
		self.direccion=address
		
		if self.direccion:
			self.figure.savefig(self.direccion+"/canvas.pdf")
			self.direccion=None
			MsgI.showinfo('importante',"Se guardó Correctamente!")
		
	def Redibujar(self):
		#MsgI.showinfo('importante',self.tiempo)
		self.figure = Figure(figsize=(11,4.7))
		fig=self.figure.add_subplot(121)
		suma=0
		suma=self.moto+self.camion+self.auto
		print("suma: ",suma)
		if suma!=0:
			#fig.title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})
			fig.text(0.0, 0.0,'Tiempo: '+str(self.tiempo),linespacing=2,color="black",weight="bold",transform=fig.transAxes,size='large')
			CantidadObjetos=[self.moto,self.camion,self.auto]
			EtiquetaObjetos=["Mototaxi","Combi","Taxi"]
			fig.pie(CantidadObjetos,labels=EtiquetaObjetos,explode=(0.05,0.05,0.05),startangle=45,shadow=True,autopct='%1.1f%%',center=(0,0))
			fig.axis('equal')
			#fig.legend(EtiquetaObjetos,loc=1)
			
		else:
			fig.text(0.1, 0.9,'Reporte No Encontrado', ha='center', va='center', transform=fig.transAxes)
		canvas = FigureCanvasTkAgg(self.figure, self.canvas)
		canvas.get_tk_widget().grid(row=0, column=0)


