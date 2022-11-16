from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import database

class UsuarioGUI(object):
	"""docstring for UsuarioGUI"""
	def __init__(self):
		self.obj_database=database.database()
	def Top_insertar(self):
		self.Top_Insertar=Toplevel()
		self.Top_Insertar.title('Ingresar Usuario')
		self.Top_Insertar.geometry('390x250')

		etiqueta=Label(self.Top_Insertar,text='Dni',font=("Arial",14))
		etiqueta.grid(row=0,column=0)
		self.Entry_Dni=ttk.Entry(self.Top_Insertar,width=40)
		self.Entry_Dni.grid(row=0,column=1,columnspan=2,pady=7)

		etiqueta=Label(self.Top_Insertar,text='Nombre',font=("Arial",14))
		etiqueta.grid(row=1,column=0)
		self.Entry_Nombre=ttk.Entry(self.Top_Insertar,width=40)
		self.Entry_Nombre.grid(row=1,column=1,columnspan=2,pady=7)

		etiqueta=Label(self.Top_Insertar,text='Apellidos',font=("Arial",14))
		etiqueta.grid(row=2,column=0)
		self.Entry_Apellidos=ttk.Entry(self.Top_Insertar,width=40)
		self.Entry_Apellidos.grid(row=2,column=1,columnspan=2,pady=7)

		etiqueta=Label(self.Top_Insertar,text='Telefono',font=("Arial",14))
		etiqueta.grid(row=3,column=0)
		self.Entry_Telefono=ttk.Entry(self.Top_Insertar,width=40)
		self.Entry_Telefono.grid(row=3,column=1,columnspan=2,pady=7)

		etiqueta=Label(self.Top_Insertar,text='Direccion',font=("Arial",14))
		etiqueta.grid(row=4,column=0)
		self.Entry_Direccion=ttk.Entry(self.Top_Insertar,width=40)
		self.Entry_Direccion.grid(row=4,column=1,columnspan=2,pady=7)


		btn_Guardar=Button(self.Top_Insertar,text='Guardar',background="deepskyblue",border=3,width=15)
		btn_Guardar['command']=self.Insertar_Usuario
		btn_Guardar.grid(row=5,column=1,pady=7)
		btn_Cancelar=Button(self.Top_Insertar,text='Cancelar',background="deepskyblue",border=3,width=15)
		btn_Cancelar['command']=self.Top_Insertar.destroy
		btn_Cancelar.grid(row=5,column=2,pady=7)
	def Insertar_Usuario(self):
		#recuperando datos
		dni=self.Entry_Dni.get()
		nombre=self.Entry_Nombre.get()
		Apellidos=self.Entry_Apellidos.get()
		telefono=self.Entry_Telefono.get()
		direccion=self.Entry_Direccion.get()
		datos=[dni,nombre,Apellidos,telefono,direccion]

		if dni.isnumeric() and len(dni)==8:
			self.obj_database.insertar_usuario(datos)
			messagebox.showinfo('Alerta','Se insertó correctamente')
			self.Top_Insertar.destroy()

		else:
			messagebox.showinfo('Alerta','Verifique el campo Dni')
			self.Top_Insertar.destroy()

	def Top_ReportePersonal(self):
		self.Windows_ReportePersonal=Toplevel()
		self.Windows_ReportePersonal.geometry('860x450')
		self.Windows_ReportePersonal.title('Reporte del Personal')
		
		etiqueta=Label(self.Windows_ReportePersonal,text='Buscar')
		etiqueta.place(x=10,y=40)
		self.Entry_sDni=ttk.Entry(self.Windows_ReportePersonal,width=40)
		self.Entry_sDni.place(x=100,y=40)
		self.table=ttk.Treeview(self.Windows_ReportePersonal,columns=('#1','#2','#3','#4','#5'),show='headings')		
		self.table.heading("#1",text="DNI")
		self.table.column("#1",width=60,anchor="center")
		self.table.heading("#2",text="NOMBRES")
		self.table.column("#2",width=200,anchor="center")
		self.table.heading("#3",text="APELLIDOS")
		self.table.column("#3",width=200,anchor="center")
		self.table.heading("#4",text="TELEFONO")
		self.table.column("#4",width=80,anchor="center")		
		self.table.heading("#5",text="DIRECCION")					
		self.table.place(x=10,y=70,width=840,height=350)
		self.LlenarTablePersonal()				
		self.Windows_ReportePersonal.focus()
		self.Windows_ReportePersonal.grab_set()
	def LlenarTablePersonal(self):
		rows=self.obj_database.consultar_Usuario()

		for i in range(len(rows)):		
			self.table.insert('','end',values=(rows[i][0],rows[i][1],rows[i][2],rows[i][3],rows[i][4]))