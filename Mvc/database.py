import sqlite3
from tkinter import messagebox
class database(object):
	"""docstring for database"""
	def __init__(self):
		#creando una base de datos
		self.conection=sqlite3.connect('data_palta.db')
		self.cursor=self.conection.cursor()

		#creando una tabla
		try:
			self.cursor.execute("""CREATE TABLE IF NOT EXISTS tableMediciones(
			id_M INTEGER  PRIMARY KEY AUTOINCREMENT,
			ancho_M REAL,
			largo_M REAL,
			peso_M REAL,
			descripcion TEXT,
			categoria TEXT)""")
		except Exception as e:
			messagebox.showinfo('Alerta',f'consulte con el administrador codigo de error : {e}')
	def insertar(self,ancho,largo,peso,descripcion,categoria):
		try:
			sql=f"INSERT INTO tableMediciones VALUES((SELECT MAX(id_M) FROM tableMediciones)+1,{ancho},{largo},{peso},'{descripcion}','{categoria}')"
			self.cursor.execute(sql)
			self.conection.commit()

		except Exception as e:
			raise e
	def consultar(self):
		try:
			self.cursor.execute('SELECT * FROM tableMediciones')
			rows=self.cursor.fetchall()
		except Exception as e:
			raise e
		return rows
	def cantidad_data(self):
		try:
			self.cursor.execute('SELECT COUNT(*) AS CANTIDAD FROM tableMediciones')
			rows=self.cursor.fetchall()

		except Exception as e:
			raise e
		return rows
	def peso_data(self):
		try:
			self.cursor.execute('SELECT SUM(peso_M) AS PESO FROM tableMediciones')
			rows=self.cursor.fetchall()

		except Exception as e:
			raise e
		return rows
	def eliminar(self):
		try:
			self.cursor.execute('DELETE FROM tableMediciones')
			self.conection.commit()

		except Exception as e:
			raise e



