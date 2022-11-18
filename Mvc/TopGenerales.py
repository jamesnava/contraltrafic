from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import database
class Categoria(object):
	"""docstring for UsuarioGUI"""
	def __init__(self):
		self.obj_database=database.database()
	def categorias(self):
		self.Top_Categoria=Toplevel()
		self.Top_Categoria.title('Categorias')
		self.Top_Categoria.geometry('900x250')
		self.table=ttk.Treeview(self.Top_Categoria,columns=('#1','#2','#3','#4','#5','#6','#7'),show='headings')
		self.table.heading("#1",text="codigo")
		self.table.column("#1",width=60,anchor="center")
		self.table.heading("#2",text="Peso Inf.")
		self.table.column("#2",width=100,anchor="center")
		self.table.heading("#3",text="Peso Sup.")
		self.table.column("#3",width=100,anchor="center")
		self.table.heading("#4",text="Zona Afect. Inf.")
		self.table.column("#4",width=150,anchor="center")		
		self.table.heading("#5",text="Zona Afect. Sup.")
		self.table.column("#5",width=150,anchor="center")
		self.table.heading("#6",text="Categoria")
		self.table.column("#6",width=150,anchor="center")
		self.table.heading("#7",text="Descripcion")
		self.table.column("#7",width=150,anchor="center")
		self.llenar_tabla_Categoria()					
		self.table.place(x=10,y=70,width=870,height=100)		


		btn_Editar=Button(self.Top_Categoria,text='Editar',background="deepskyblue",border=3,width=15)		
		btn_Editar.bind('<Button-1>',self.Top_Update)
		btn_Editar.place(x=100,y=200)
		btn_Cancelar=Button(self.Top_Categoria,text='Cancelar',background="deepskyblue",border=3,width=15)
		btn_Cancelar['command']=self.Top_Categoria.destroy
		btn_Cancelar.place(x=450,y=200)
		self.Top_Categoria.grab_set()
	def llenar_tabla_Categoria(self):
		rows=self.obj_database.consultar_calibre()	
		if rows!=None:
			for i in range(len(rows)):
				self.table.insert('','end',values=(rows[i][0],rows[i][1],rows[i][2],rows[i][3],rows[i][4],rows[i][5],rows[i][6]))

	def Top_Update(self,event):
		codi=''
		try:
			codi=self.table.item(self.table.selection()[0],option='values')[0]
		except Exception as e:
			messagebox.showerror('Mensaje de Error','Seleccione un Item')

		if len(codi)!=0:
			#recuperando valores de la tabla
			peso_Inferior=self.table.item(self.table.selection()[0],option='values')[1]
			peso_Superior=self.table.item(self.table.selection()[0],option='values')[2]
			zona_Inferior=self.table.item(self.table.selection()[0],option='values')[3]
			zona_Superior=self.table.item(self.table.selection()[0],option='values')[4]
			Categoria=self.table.item(self.table.selection()[0],option='values')[5]
			descripcion=self.table.item(self.table.selection()[0],option='values')[6]
			#fin valores de la tabla
			self.Top_UCategoria=Toplevel()
			self.Top_UCategoria.title('Categorias')
			self.Top_UCategoria.geometry('500x400')
			self.Top_UCategoria.resizable(0,0)
			self.Top_UCategoria.grab_set()
			etiqueta=Label(self.Top_UCategoria,text='Codigo',font=("Arial",14))
			etiqueta.grid(row=0,column=0)
			self.Entry_codigo=ttk.Entry(self.Top_UCategoria,width=40)
			self.Entry_codigo.insert('end',f'{codi}')
			self.Entry_codigo.config(state='readonly')
			self.Entry_codigo.grid(row=0,column=1,columnspan=2,pady=7)

			etiqueta=Label(self.Top_UCategoria,text='Peso. Inf.',font=("Arial",14))
			etiqueta.grid(row=1,column=0)
			self.Entry_PesoInf=ttk.Entry(self.Top_UCategoria,width=40)
			self.Entry_PesoInf.insert('end',f'{peso_Inferior}')

			self.Entry_PesoInf.grid(row=1,column=1,columnspan=2,pady=7)

			etiqueta=Label(self.Top_UCategoria,text='Peso. Sup.',font=("Arial",14))
			etiqueta.grid(row=2,column=0)
			self.Entry_PesoSup=ttk.Entry(self.Top_UCategoria,width=40)
			self.Entry_PesoSup.insert('end',f'{peso_Superior}')
			self.Entry_PesoSup.grid(row=2,column=1,columnspan=2,pady=7)

			etiqueta=Label(self.Top_UCategoria,text='Zona Aft. inf',font=("Arial",14))
			etiqueta.grid(row=3,column=0)
			self.Entry_ZonaAftInf=ttk.Entry(self.Top_UCategoria,width=40)
			self.Entry_ZonaAftInf.insert('end',f'{zona_Inferior}',)
			self.Entry_ZonaAftInf.grid(row=3,column=1,columnspan=2,pady=7)

			etiqueta=Label(self.Top_UCategoria,text='Zona Aft. Sup',font=("Arial",14))
			etiqueta.grid(row=4,column=0)
			self.Entry_ZonaAftSup=ttk.Entry(self.Top_UCategoria,width=40)
			self.Entry_ZonaAftSup.insert('end',zona_Superior)
			self.Entry_ZonaAftSup.grid(row=4,column=1,columnspan=2,pady=7)

			etiqueta=Label(self.Top_UCategoria,text='Denominación',font=("Arial",14))
			etiqueta.grid(row=5,column=0)
			self.Entry_Denominacion=ttk.Entry(self.Top_UCategoria,width=40)
			self.Entry_Denominacion.insert('end',f'{Categoria}')
			self.Entry_Denominacion.config(state='readonly')
			self.Entry_Denominacion.grid(row=5,column=1,columnspan=2,pady=7)

			etiqueta=Label(self.Top_UCategoria,text='Descripción',font=("Arial",14))
			etiqueta.grid(row=6,column=0)
			self.Entry_Descipcion=ttk.Entry(self.Top_UCategoria,width=40)
			self.Entry_Descipcion.insert('end',f'{descripcion}')
			self.Entry_Descipcion.grid(row=6,column=1,columnspan=2,pady=7)



			btn_Guardar=Button(self.Top_UCategoria,text='Guardar',background="deepskyblue",border=3,width=15)
			btn_Guardar['command']=self.Actualizar_Categoria
			btn_Guardar.grid(row=7,column=1,pady=10)
			btn_Cancelar=Button(self.Top_UCategoria,text='Cancelar',background="deepskyblue",border=3,width=15)
			btn_Cancelar['command']=self.Top_UCategoria.destroy
			btn_Cancelar.grid(row=7,column=2,pady=10)

	def Actualizar_Categoria(self):
		self.Entry_codigo['state']='NORMAL'
		codigo=self.Entry_codigo.get()
		peso_inf=self.Entry_PesoInf.get()
		peso_sup=self.Entry_PesoSup.get()
		zonaAftInf=self.Entry_ZonaAftInf.get()
		zonaAftSup=self.Entry_ZonaAftSup.get()
		descripcion=self.Entry_Descipcion.get()

		#actualizando
		self.obj_database.update_calibre(codigo,peso_sup,peso_inf,zonaAftInf,zonaAftSup,descripcion)
		self.Top_UCategoria.destroy()

	def Top_Precio(self):
		pass






		

		
	