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

			#creando la tabla usuario
			self.cursor.execute("""
				CREATE TABLE IF NOT EXISTS usuario(				
				dni TEXT,
				nombre TEXT,
				apellidos TEXT,
				telefono TEXT,
				direccion TEXT				
				)
				""")

			self.cursor.execute("""CREATE TABLE IF NOT EXISTS tableMediciones(
			id_M INTEGER  PRIMARY KEY AUTOINCREMENT,
			ancho_M REAL,
			largo_M REAL,
			peso_M REAL,
			descripcion TEXT,
			categoria TEXT,
			fecha date,
			areaTotal REAL,
			areaLimpia REAL,
			dni TEXT,
			FOREIGN KEY (dni) REFERENCES usuario(dni)
			)""")
			
		except sqlite3.Error as e:
			messagebox.showinfo('Alerta',f'consulte con el administrador codigo de error : {e}')

	def insertar_mediciones(self,ancho,largo,peso,descripcion,categoria,fecha,areaTotal,areaLimpia,dni):
		try:
			sql=f"INSERT INTO tableMediciones VALUES((SELECT MAX(id_M) FROM tableMediciones)+1,{ancho},{largo},{peso},'{descripcion}','{categoria}','{fecha}',{areaTotal},{areaLimpia},'{dni}')"
			self.cursor.execute(sql)
			self.conection.commit()

		except Exception as e:
			raise e
	def consultar_UserMediciones(self,dni):
		pass
	def consultar_mediciones(self):
		try:
			self.cursor.execute('SELECT * FROM tableMediciones')
			rows=self.cursor.fetchall()
		except Exception as e:
			raise e
		return rows
	def cantidad_datamediciones(self):
		try:
			self.cursor.execute('SELECT COUNT(*) AS CANTIDAD FROM tableMediciones')
			rows=self.cursor.fetchall()

		except Exception as e:
			raise e
		return rows
	def peso_datamediciones(self):
		try:
			self.cursor.execute('SELECT SUM(peso_M) AS PESO FROM tableMediciones')
			rows=self.cursor.fetchall()

		except Exception as e:
			raise e
		return rows
	def eliminar_datamediciones(self):
		try:
			self.cursor.execute('DELETE FROM tableMediciones')
			self.conection.commit()

		except Exception as e:
			raise e
	def insertar_usuario(self,datos):
		try:
			self.cursor.execute(f"""INSERT INTO usuario VALUES('{datos[0]}','{datos[1]}','{datos[2]}','{datos[3]}','{datos[4]}')""")
			self.conection.commit()
		except Exception as e:
			raise e
	def consultar_Usuario(self):
		try:
			self.cursor.execute('SELECT * FROM usuario')
			rows=self.cursor.fetchall()
		except Exception as e:
			raise e
		return rows
	def consultar_dni(self,dni):
		try:
			self.cursor.execute(f"SELECT count(*) FROM usuario WHERE dni='{dni}'")
			rows=self.cursor.fetchall()			
		except Exception as e:
			raise e
		return rows		


