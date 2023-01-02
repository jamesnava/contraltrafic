import joblib
from tkinter import *
import joblib
import timeit
import dataclasses
import threadpoolctl

class ventana(object):
	"""docstring for ventana"""
	def __init__(self):
		self.ventana=Tk()
		self.ventana.geometry('400x400')
		self.etiqueta=Label(self.ventana,text='resultado')
		self.etiqueta.place(x=10,y=100)
		largo=11
		ancho=10
		modelo=joblib.load('modelo.joblib')
		area=int(largo)*int(ancho)
		peso=modelo.predict([[area]])
		self.etiqueta.config(text=str(peso))
		self.ventana.mainloop()
	
		
obj=ventana()