import tkinter as tk
from tkinter import ttk
import VMain

class BuscarCamara:
	"""docstring for ClassName"""
	ventana=None
	def __init__(self):
		self.ventana=tk.Tk()
		self.ventana.wm_attributes("-topmost",1)
		self.ventana.geometry("100x100")
	def salir(self):
		objPrincipal=VMain.VMain()
		objPrincipal.ventana.wv_attributes("-disabled",0)

	def ejecutarVentana(self):
		self.ventana.protocol("WM_DELETE_WINDOW",self.salir)
		self.ventana.mainloop()

		
		