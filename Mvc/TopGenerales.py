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
		self.Top_Categoria.iconbitmap('../images/categoria.ico')
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
				self.table.insert('','end',values=(rows[i][0],rows[i][2],rows[i][1],rows[i][3],rows[i][4],rows[i][5],rows[i][6]))

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
		self.Top_precio=Toplevel()
		self.Top_precio.title('Precios por categorias')
		self.Top_precio.iconbitmap('../images/precio.ico')
		self.Top_precio.geometry('550x250')
		self.tablePrecio=ttk.Treeview(self.Top_precio,columns=('#1','#2','#3','#4'),show='headings')
		self.tablePrecio.heading("#1",text="Codigo")
		self.tablePrecio.column("#1",width=60,anchor="center")
		self.tablePrecio.heading("#2",text="Categoria")
		self.tablePrecio.column("#2",width=100,anchor="center")
		self.tablePrecio.heading("#3",text="Precio S/.")
		self.tablePrecio.column("#3",width=100,anchor="center")
		self.tablePrecio.heading("#4",text="Unidad")
		self.tablePrecio.column("#4",width=100,anchor="center")				
		self.tablePrecio.place(x=10,y=70,width=520,height=100)		

		self.llenar_tabla_Precio()
		btn_EditarPrecio=Button(self.Top_precio,text='Editar',background="deepskyblue",border=3,width=15)		
		btn_EditarPrecio.bind('<Button-1>',self.Top_UpdatePrecio)
		btn_EditarPrecio.place(x=100,y=200)
		btn_CancelarPrecio=Button(self.Top_precio,text='Cancelar',background="deepskyblue",border=3,width=15)
		btn_CancelarPrecio['command']=self.Top_precio.destroy
		btn_CancelarPrecio.place(x=300,y=200)
		self.Top_precio.grab_set()

	def llenar_tabla_Precio(self):
		rows=self.obj_database.consultar_precios()	
		if rows!=None:
			for i in range(len(rows)):
				self.tablePrecio.insert('','end',values=(rows[i][0],rows[i][1],rows[i][2],rows[i][3]))

	def Top_UpdatePrecio(self,event):
		codi=''
		try:
			codi=self.tablePrecio.item(self.tablePrecio.selection()[0],option='values')[0]
		except Exception as e:
			messagebox.showerror('Mensaje de Error','Seleccione un Item')

		if len(codi)!=0:
			#recuperando valores de la tabla
			precio=self.tablePrecio.item(self.tablePrecio.selection()[0],option='values')[2]
			cate=self.tablePrecio.item(self.tablePrecio.selection()[0],option='values')[1]			
			#fin valores de la tabla
			self.Top_UPrecio=Toplevel()
			self.Top_UPrecio.title('Actualizar precio')
			self.Top_UPrecio.geometry('500x200')
			self.Top_UPrecio.resizable(0,0)
			self.Top_UPrecio.grab_set()
			etiqueta=Label(self.Top_UPrecio,text='Codigo',font=("Arial",14))
			etiqueta.grid(row=0,column=0)
			self.Entry_cod=ttk.Entry(self.Top_UPrecio,width=40)
			self.Entry_cod.insert('end',f'{codi}')
			self.Entry_cod.config(state='readonly')
			self.Entry_cod.grid(row=0,column=1,columnspan=2,pady=7)

			etiqueta=Label(self.Top_UPrecio,text='Categoria',font=("Arial",14))
			etiqueta.grid(row=1,column=0)
			self.Entry_cate=ttk.Entry(self.Top_UPrecio,width=40)
			self.Entry_cate.insert('end',f'{cate}')
			self.Entry_cate.config(state='readonly')
			self.Entry_cate.grid(row=1,column=1,columnspan=2,pady=7)

			etiqueta=Label(self.Top_UPrecio,text='Precio',font=("Arial",14))
			etiqueta.grid(row=2,column=0)
			self.Entry_precio=ttk.Entry(self.Top_UPrecio,width=40)
			self.Entry_precio.insert('end',f'{precio}')			
			self.Entry_precio.grid(row=2,column=1,columnspan=2,pady=7)

			btn_GuardarPrecio=Button(self.Top_UPrecio,text='Guardar',background="deepskyblue",border=3,width=15)
			btn_GuardarPrecio['command']=self.Actualizar_precio
			btn_GuardarPrecio.grid(row=3,column=1,pady=10)
			btn_CancelarPrecio=Button(self.Top_UPrecio,text='Cancelar',background="deepskyblue",border=3,width=15)
			btn_CancelarPrecio['command']=self.Top_UPrecio.destroy
			btn_CancelarPrecio.grid(row=3,column=2,pady=10)

	def Actualizar_precio(self):
		self.Entry_cod['state']='NORMAL'
		cod=self.Entry_cod.get()
		precio=self.Entry_precio.get()
		#actualizando
		if self.is_float_digit(precio):
			self.obj_database.update_precio(cod,precio)
		else:
			messagebox.showerror('Alerta','Valor no permitido')
		self.Top_UPrecio.destroy()
		self.Top_precio.destroy()

	def is_float_digit(self,n: str) -> bool:
		try:
			float(n)
			return True
		except ValueError:
			return False



		

		
	