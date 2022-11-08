import database
from tkinter import messagebox
class Estadisticas(object):
	"""docstring for Estadisticas"""
	def __init__(self):
		self.obj_database=database.database()
	def Vaciar_Data(self):
		valor=messagebox.askquestion(message='Estas seguro que quiere eliminar la data?',title='Alerta')
		if valor=='yes':
			self.obj_database.eliminar()
			messagebox.showinfo('Alerta','Se vació la data')
	def Insertar_Data(self,datos):
		self.obj_database.insertar(datos[0],datos[1],datos[2],datos[3],datos[4])
		

		