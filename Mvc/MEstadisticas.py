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
		self.obj_database.insertar_mediciones(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7],datos[8])
	def Cantidad_Analizado(self):
		rows=self.obj_database.cantidad_datamediciones()
		return rows[0][0]
	def peso_Total(self):
		rows=self.obj_database.peso_datamediciones()
		return rows[0][0]
	def dni_user(self,dni):
		rows=self.obj_database.consultar_dni(dni)
		return rows[0][0]
	def Asignacion_Calibre(self,peso,area):
		rows=self.obj_database.consultar_calibre()
		rows1=self.obj_database.consultar_calibre()
		
		datos=[]
		pesos=[]
		for j in range(len(rows1)):
			datos.append(rows1[j][4])
			pesos.append(rows1[j][2])
		codigo=''
		Categoria=''
		
		for i in range(len(rows)):
			#print(rows[i][2],rows[i][1],rows[i][3],rows[i][4])

			if (rows[i][2]<=peso and rows[i][4]>=area) and int(rows[i][0])==1:
				codigo=rows[i][0]
				Categoria=rows[i][6]
			elif (rows[i][2]<=peso and peso<rows[i][1]) and area<=rows[i][4] and int(rows[i][0])==2:
				codigo=rows[i][0]
				Categoria=rows[i][6]

			elif ((rows[i][2]<=peso and peso<rows[i][1]) and area<=rows[i][4] and int(rows[i][0])==3):
				codigo=rows[i][0]
				Categoria=rows[i][6]

			elif ((peso>=rows[i][1]) and int(rows[i][0])==2) and (datos[0]<area<=datos[1]):
				codigo=rows[i][0]
				Categoria=rows[i][6]

			elif ((peso>rows[i][1]) and int(rows[i][0])==3) and (datos[1]<area<=datos[2]):
				codigo='3'
				Categoria='Se considera de Tercera'

			elif ((pesos[1]>peso>rows[i][1]) and int(rows[i][0])==3) and (area<=datos[2]):
				codigo=rows[i][0]
				Categoria=rows[i][6]
			
		return codigo,Categoria




		

		