import database
from tkinter import messagebox
class Estadisticas(object):
	"""docstring for Estadisticas"""
	def __init__(self):
		self.obj_database=database.database()
	def Vaciar_Data(self,label):
		valor=messagebox.askquestion(message='Estas seguro que quiere eliminar la data?',title='Alerta')
		if valor=='yes':
			self.obj_database.eliminar_datamediciones()
			messagebox.showinfo('Alerta','Se vació la data')
			#print(label)
			cantidad=self.Cantidad_Analizado()
			font_=('Courier',16,'bold')
			label.config(text=f"Analizados: {cantidad} Paltas",font=font_,bg='#19330E',fg='white')

	def Insertar_Data(self,datos):
		self.obj_database.insertar_mediciones(datos[0],datos[1],datos[2],datos[3],datos[4])
	def Cantidad_Analizado(self):
		rows=self.obj_database.cantidad_datamediciones()
		return rows[0][0]
	def peso_Total(self):
		rows=self.obj_database.peso_datamediciones()
		return rows[0][0]
		

		