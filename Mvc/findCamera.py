import tkinter as tk
from tkinter import ttk
import VMain

class BuscarCamara:
	"""docstring for ClassName"""
	ventana=None
	def __init__(self):
		self.numeroCamera=None
	def Top_Camera(self):
		self.top1 = tk.Toplevel(bg="Orange",relief="groove")
		self.top1.title("Seeleccionar Cámara")
		self.top1.geometry("500x170+200+120")
		self.top1.overrideredirect(1)
		self.top1.wm_attributes("-topmost",1)		

		labelCamara=tk.Label(self.top1,text="Seleccione una Cámara:")
		labelCamara.configure(width=20,bg="Orange",font=("",14),height=3)
		labelCamara.place(x=0,y=20)

		#agregando un select...
		self.selectCamara=ttk.Combobox(self.top1,font=("",14),height=3)
		self.selectCamara["values"]=[0,1,2,3,4,5,6,7,8,9]
		self.selectCamara.current(0)
		self.selectCamara.place(x=250,y=40)
		#agregando un boton...
		botonAceptar=tk.Button(self.top1,text="Aceptar",bg="#FFF",font=("",14))
		botonAceptar.configure(width=9,command=self.event_Selection)
		botonAceptar.place(x=160,y=100)
		self.top1.grab_set()
		#self.top1.mainloop()
	def event_Selection(self):
		self.numeroCamera=self.selectCamara.get()
		self.top1.destroy()
		

	

		
		