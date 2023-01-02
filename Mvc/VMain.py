import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2
import numpy as np
import threading 
import tkinter.messagebox as msgI
from tkinter.simpledialog import askstring
#clases...
import Fotogramas
import Report
import findCamera
import MEstadisticas
import usuario
import TopGenerales
import datetime

class VMain(object):	
	objVideo=None	
	def __init__(self):		
		self.fechap=datetime.date.today()
		self.numeroCamara=None
		self.hilo=False
		self.matriz_Image=None
		self.cap=None
		self.Address_video=None
		self.imageComprobar=False
		#creando objetos
		self.obj_Camera=findCamera.BuscarCamara()
		self.objVideo=Fotogramas.camara()
		self.obj_Estadisticas=MEstadisticas.Estadisticas()
		self.usuario=usuario.UsuarioGUI()
		self.obj_reporte=Report.Reports()
		self.obj_TopGeneral=TopGenerales.Categoria()
		self.controlador_video=0
		#configuracion basica de la ventana
		self.ventana=tk.Tk()
		self.ventana.title("SISTEMA DE CLASIFICACION DE LA PALTA")
		screen_width = self.ventana.winfo_screenwidth()
		screen_height = self.ventana.winfo_screenheight()
		self.ventana.geometry(f'{int(screen_width*0.99)}x{int(screen_height*0.90)}+0+0')
		#self.ventana.overrideredirect(1)
		self.ventana.protocol("WM_DELETE_WINDOW",lambda:self.EventoMSalir(self.cap))
		self.ventana.iconbitmap('images/favicon.ico')
		#self.ventana.resizable(0,0)
		self.ventana.configure(bg="#121F39")
		#agregando marco izquierda
		self.Marco=tk.Frame(self.ventana,width=130,height=int(screen_height*0.75))
		self.Marco.place(x=10,y=10)		
		#self.Marco.config(bg="#121F39")
		self.Marco.config(relief='groove')
		self.Marco.config(bd=3)

		#insertando los botones...
		#titulo1 del menu izquierdo...
		self.etiquetaTitulo1=tk.Label(self.Marco,text="Imágenes")
		self.etiquetaTitulo1.configure(fg="#fff",bg="#BF4262",font=("Helvetica",14,"bold","italic"),width=11,height=1,bd=2,relief="groove")
		self.etiquetaTitulo1.place(x=-5,y=20)
		#Abrir y cargar imagenes...
		colorboton="#07755A"

		self.openVideo=tk.Button(self.Marco,text="Buscar",fg="#fff",bg=colorboton,font=("",14),height=3,cursor="hand2")
		self.openVideo.configure(command=lambda:self.abrirDireccion(self.hilo),bd=5,overrelief="sunken",width=9)

		self.openVideo.bind('<Motion>',lambda event,param=self.openVideo:self.EventsMotions(event,param))
		self.openVideo.bind('<Leave>',lambda event,param=self.openVideo:self.EventsLeave(event,param))
		self.openVideo.place(x=5,y=60)
		
		self.reproducirO=tk.Button(self.Marco,text="Cargar",fg="#fff",bg=colorboton,font=("",14),height=3,cursor="hand2")
		self.reproducirO.configure(command=self.abrirImagen,bd=5,overrelief="raised")

		self.reproducirO.bind('<Motion>',lambda event,param=self.reproducirO:self.EventsMotions(event,param))
		self.reproducirO.bind('<Leave>',lambda event,param=self.reproducirO:self.EventsLeave(event,param))
		self.reproducirO.configure(width=9)
		self.reproducirO.place(x=5,y=160)
		#agregar separador...
		#estilo del separador...
		
		separador1Left=ttk.Separator(self.Marco,orient="horizontal")
		separador1Left.place(x=0,y=255,relwidth=5)
		#titulo2
		self.etiquetaTitulo2=tk.Label(self.Marco,text="En Vivo")
		self.etiquetaTitulo2.configure(fg="#fff",bg="#BF4262",font=("Helvetica",14,"bold","italic"),width=11,height=1,bd=2,relief="groove")
		self.etiquetaTitulo2.place(x=-5,y=255)

		self.Bconfigurar=tk.Button(self.Marco,text="Selec. Cam.",fg="#fff",bg=colorboton,font=("",14),height=3,cursor="hand2")
		self.Bconfigurar.configure(width=9)
		self.Bconfigurar.configure(command=self.obj_Camera.Top_Camera,bd=5,overrelief="raised")
		self.Bconfigurar.bind('<Motion>',lambda event,param=self.Bconfigurar:self.EventsMotions(event,param))
		self.Bconfigurar.bind('<Leave>',lambda event,param=self.Bconfigurar:self.EventsLeave(event,param))
		self.Bconfigurar.place(x=5,y=300)

		#play
		self.BIniciar=tk.Button(self.Marco,text="Iniciar",fg="#fff",bg=colorboton,font=("",14),height=3,cursor="hand2")
		self.BIniciar.configure(width=9,command=self.InicioVideo,bd=5,overrelief="raised")
		self.BIniciar.bind('<Motion>',lambda event,param=self.BIniciar:self.EventsMotions(event,param))
		self.BIniciar.bind('<Leave>',lambda event,param=self.BIniciar:self.EventsLeave(event,param))
		self.BIniciar.place(x=5,y=395)		

		self.BTerminar=tk.Button(self.Marco,text="Liberar Cam.",fg="#fff",bg=colorboton,font=("",14),height=3,cursor="hand2")
		self.BTerminar.configure(command=self.CapturaImagen,bd=5,overrelief="raised")
		self.BTerminar.bind('<Motion>',lambda event,param=self.BTerminar:self.EventsMotions(event,param))
		self.BTerminar.bind('<Leave>',lambda event,param=self.BTerminar:self.EventsLeave(event,param))
		self.BTerminar.configure(width=9)
		self.BTerminar.place(x=5,y=489)

		

		#fin de izquierdo
		#agregando marco principal
		self.MarcoP=tk.Frame(self.ventana,width=int(screen_width*0.89),height=int(screen_height*.75))
		self.MarcoP.config(relief='ridge')
		self.MarcoP.config(bd=3)
		self.MarcoP.place(x=int(screen_width*0.11),y=10)
		#Label video
		formato=('Segoe Script',14,"bold","italic")
		
		etiqueta_titulo_cuadro1=tk.Label(self.MarcoP,text="Imagen Original",fg='indigo',font=formato)
		etiqueta_titulo_cuadro1.place(x=22,y=1)

		self.EtiquetaVideo=tk.Label(self.MarcoP,text="Imagen original",font=('Times',14,"bold","italic"),bg="#232928",fg="#fff",bd=5,relief="sunken")
		self.EtiquetaVideo.config(width="26",height="9")	
		self.EtiquetaVideo.place(x=10,y=30)
		
		#etiqueta imagen binarizada
		etiqueta_titulo_cuadro2=tk.Label(self.MarcoP,text="Binarizada",fg='indigo',font=formato)
		etiqueta_titulo_cuadro2.place(x=420,y=1)

		self.EtiquetaIBinarizada=tk.Label(self.MarcoP,text="Imagen ",font=('Times',14,"bold","italic"),bg="#232928",fg="#fff",relief="sunken")
		self.EtiquetaIBinarizada.config(width="26",height="9")
		self.EtiquetaIBinarizada.place(x=420,y=30)

		#etiqueta 3ra imagen
		etiqueta_titulo_cuadro3=tk.Label(self.MarcoP,text="Analisis de color",font=formato,fg='indigo')
		etiqueta_titulo_cuadro3.place(x=870,y=1)
		self.EtiquetaImagen3=tk.Label(self.MarcoP,text="Imagen 2",font=('Times',14,"bold","italic"),bg="#232928",fg="#fff",relief="sunken")
		self.EtiquetaImagen3.config(width="26",height="9")
		self.EtiquetaImagen3.place(x=850,y=30)
		
		#img_btnProcess=tk.PhotoImage(file=r'../images/process_btn.png')
		#img_btnProcess.subsample(3,3)
		btn_process=tk.Button(self.MarcoP,text='Procesar',border=3,width=25,cursor='hand2',background="deepskyblue")
		btn_process.config(command=self.deteccion_bordes)
		btn_process.place(x=500,y=280)

		#agregando la tabla
		self.Tabla_General=ttk.Treeview(self.MarcoP,columns=('#1','#2','#3','#4','#5'),show='headings')
		self.Tabla_General.heading('#1',text='Largo (cm)')
		self.Tabla_General.heading('#1',anchor='center')
		self.Tabla_General.heading('#2',text='Ancho (cm)')
		self.Tabla_General.heading('#2',anchor='center')
		self.Tabla_General.heading('#3',text='Peso Estimado (Gramos)')
		self.Tabla_General.heading('#3',anchor='center')
		self.Tabla_General.heading('#4',text='Estado de Producto')
		self.Tabla_General.heading('#4',anchor='center')
		self.Tabla_General.heading('#5',text='Clasificación')
		self.Tabla_General.heading('#5',anchor='center')
		self.Tabla_General.place(x=10,y=370,width=1150,height=200)
		#marco bottom
		self.MarcoBottom=tk.Frame(self.ventana,width=int(screen_width*0.967),height=80)
		
		self.MarcoBottom.config(bg="#19330E")
		self.MarcoBottom.config(relief='ridge')
		self.MarcoBottom.config(bd=3)

		self.MarcoBottom.place(x=10,y=int(screen_height*0.77))
			
		
		#Leyenda
		font_=('Courier',16,'bold')
		cantidad=self.obj_Estadisticas.Cantidad_Analizado()
		self.Cantidad_Palta=tk.Label(self.MarcoBottom,text=f"Analizados: {cantidad} Paltas",font=font_,bg='#19330E',fg='white')
		self.Cantidad_Palta.place(x=5,y=20)		
		peso=self.obj_Estadisticas.peso_Total()
		if peso==None:
			peso=0		
		self.Peso_Total=tk.Label(self.MarcoBottom,text=f"Peso Total: {round(peso/1000,2)} KG",font=font_,bg='#19330E',fg='white')
		self.Peso_Total.place(x=300,y=20)	

		self.EtiquetaUser=tk.Label(self.MarcoBottom,text="NULL",font=('Courier',14,"bold","italic"))
		self.EtiquetaUser.place(x=int(screen_width*0.75),y=20)
		self.BarraMenu()
		#hilo
		
		#inicializar la camara...

	def EventsMotions(self,event,param):
		param.config(relief='sunken',background='#94B2C7',fg='#000',bd=5)
	def EventsLeave(self,event,param):
		param.config(relief='raised',bd=5,background='#07755A',fg='#fff')


	def BarraMenu(self):
		self.BarraMenu=tk.Menu(self.ventana)
		self.ventana.config(menu=self.BarraMenu)
		#creando submenues Ayuda.
		AyudaM=tk.Menu(self.BarraMenu,tearoff=0)
		AyudaM.add_command(label="Autor",command=self.informacionAutor)
		AyudaM.add_command(label="Acerca de...",command= self.informacionSoftware)
		#menú configuracion...
		ConfiguracionM=tk.Menu(self.BarraMenu,tearoff=0)
		ConfiguracionM.add_command(label="Configurar Precio",command=self.obj_TopGeneral.Top_Precio)
		ConfiguracionM.add_command(label="Cargar Categorias Palta",command=self.obj_TopGeneral.categorias)
		ConfiguracionM.add_command(label="Configurar Propietario",command=self.config_Usuario)
		ConfiguracionM.add_command(label="Cargar Video",command=lambda:self.abrirDireccion(self.hilo))
		ConfiguracionM.add_command(label="Minimizar",command=lambda :self.ventana.iconify())
		ConfiguracionM.add_command(label="Salir",command=lambda:self.EventoMSalir(self.cap))

		#data
		Menu_data=tk.Menu(self.BarraMenu,tearoff=0)
		Menu_data.add_command(label="Estadisticas",command=self.obj_reporte.Dibujar_Reporte)
		Menu_data.add_command(label='Vaciar Data',command=self.vaciar_data)

		#personal
		Menu_personal=tk.Menu(self.BarraMenu,tearoff=0)
		Menu_personal.add_command(label="Insertar Nuevo",command=self.usuario.Top_insertar)
		Menu_personal.add_command(label='Reporte del Personal',command=self.usuario.Top_ReportePersonal)
		#agregando los menues...
		
		self.BarraMenu.add_cascade(label="Configuraciones",menu=ConfiguracionM)
		self.BarraMenu.add_cascade(label='Reportes',menu=Menu_data)
		self.BarraMenu.add_cascade(label='Personal',menu=Menu_personal)
		self.BarraMenu.add_cascade(label="Ayuda",menu=AyudaM)
	def vaciar_data(self):
		self.obj_Estadisticas.Vaciar_Data(self.Cantidad_Palta)

	def config_Usuario(self):
		dni=askstring('Configurar Usuario','Ingrese el numero de su Dni: \t\t')
		if self.obj_Estadisticas.dni_user(dni)!=0:
			self.EtiquetaUser['text']=dni
		else:
			msgI.showinfo('Alerta','DNI no encontrado, Registre en el apartado Personal')

	def AbrirFotogramas(self,mirror=False):
		if self.numeroCamara!=None:				
			self.cap=cv2.VideoCapture(int(self.numeroCamara),cv2.CAP_DSHOW)											
			while (self.cap.isOpened()):
				ret,FrameMatriz_original=self.cap.read()
				if ret:
					FrameMatriz_scalado=cv2.resize(FrameMatriz_original,(int(FrameMatriz_original.shape[1]*0.50),int(FrameMatriz_original.shape[0]*0.50)),interpolation=cv2.INTER_AREA)			
					self.matriz_Image=FrameMatriz_original
					fotograma=self.objVideo.lectura(FrameMatriz_scalado)
					self.EtiquetaVideo.config(width="320",height="240")
					self.EtiquetaVideo.configure(image=fotograma)
					self.EtiquetaVideo.image=fotograma
					if self.hilo:					
						self.hilo=False					
						break
			self.cap.release()
			self.cap=None				
		else:
			msgI.showinfo("Alerta!!","Seleccione Camara!!")

	def InicioVideo(self):
		if self.EtiquetaUser.cget('text')!='NULL':			
			self.numeroCamara=self.obj_Camera.numeroCamera		
			self.manejador=threading.Thread(target=self.AbrirFotogramas)
			self.manejador.start()
		else:
			msgI.showinfo('Alerta','Configure Propietario')

	def CapturaImagen(self):		
		self.hilo=True	

	def EventoMSalir(self,cap):
		if self.cap==None:
			self.ventana.destroy()
		else:
			msgI.showinfo("Alerta!","Antes Presione el Boton Parar!!")

	def abrirDireccion(self,hilo):
		if self.EtiquetaUser.cget('text')!='NULL':
			hilo=True
			self.Address_video=filedialog.askopenfilename()
		else:
			msgI.showinfo('Alerta','Configure Propietario')

	def abrirImagen(self):
		if self.Address_video!=None:
			self.imageComprobar=True
			img_source=cv2.imread(self.Address_video)
			img_source=cv2.cvtColor(img_source,cv2.COLOR_BGR2RGB)
			#redimencionar para procesar
			img_source=cv2.resize(img_source,(640,480),interpolation=cv2.INTER_AREA)
			self.matriz_Image=img_source			
			img_source=cv2.resize(img_source,(int(img_source.shape[1]*0.5),int(img_source.shape[0]*0.5)),interpolation=cv2.INTER_AREA)
			
			img_source=self.objVideo.lectura(img_source)
			self.EtiquetaVideo.config(width="320",height="240")
			self.EtiquetaVideo.configure(image=img_source)
			self.EtiquetaVideo.image=img_source
		
					
	def deteccion_bordes(self):
		if self.imageComprobar:
			img=self.matriz_Image
			img1=img				
			img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)				
			#redimensionando las imagenes
			img=self.objVideo.redimensionar_image(img)
			img1=self.objVideo.redimensionar_image(img1)

			img=self.objVideo.detected_edges(self.objVideo.desenfoque(img))
			largo,ancho,cordenadas=self.objVideo.encontrar_contorno(img)
		
			#prediccion del peso de la palta
			peso_palta=self.objVideo.Prediccion_peso(round(largo/13.42,3),round(ancho/13.42,3))		
		
			img=self.objVideo.dibujar_delimitador(img,cordenadas,largo,ancho)
			img=self.objVideo.formato_Tkinter(img)
			self.EtiquetaIBinarizada.config(width='320',height='240')
			self.EtiquetaIBinarizada.configure(image=img)
			self.EtiquetaIBinarizada.image=img

			#analisis de color
			img1,area_total,area_parcial=self.objVideo.analisis_Color(img1)
			img1=self.objVideo.formato_Tkinter(img1)
			self.EtiquetaImagen3.config(width='320',height='240')
			self.EtiquetaImagen3.configure(image=img1)
			self.EtiquetaImagen3.image=img1
			porcentaje_Verde=area_parcial/area_total
			porcentaje_Verde=round(porcentaje_Verde,2)
			if porcentaje_Verde>1:
				porcentaje_Verde=1
			porcentaje_ZonaAfectada=1-porcentaje_Verde
		

			#se formatea la fecha actual
			#fecha=f'{self.fecha_actual.year}-{self.fecha_actual.month}-{self.fecha_actual.day}'
			fecha=self.fechap
			#print(self.fechap)
			peso=self.obj_Estadisticas.peso_Total()
		
			if peso==None:
				peso=0.0
		
			peso=round(peso/1000,2)
			codi_calibre,categoria=self.obj_Estadisticas.Asignacion_Calibre(peso_palta,round(porcentaje_ZonaAfectada*100,3))

			if len(codi_calibre)!=0 and len(categoria)!=0:
				#ingresando a la base de datos
				datos=[ancho,largo,round(peso_palta[0][0],2),categoria,fecha,area_total,area_parcial,self.EtiquetaUser.cget('text'),codi_calibre]
				self.obj_Estadisticas.Insertar_Data(datos)
				cantidad=self.obj_Estadisticas.Cantidad_Analizado()
		
				descripcion=f'La zona afectada representa el {round(porcentaje_ZonaAfectada*100,3)}%'
				self.datos_Table(largo,ancho,round(peso_palta[0][0],1),descripcion,categoria)
				font_=('Courier',16,'bold')
				self.Cantidad_Palta.config(text=f"Analizados: {cantidad} Paltas",font=font_,bg='#19330E',fg='white')
				self.Peso_Total.config(text=f"Peso Total: {peso} KG",font=font_,bg='#19330E',fg='white')
			else:
				msgI.showinfo('Notificacion','No se considera en ninguna categoria')
		else:
			msgI.showinfo('Notificación','Seleccione una imagen')
			
	def datos_Table(self,largo,ancho,peso,descripcion,categoria):
		largo=round(largo/13.42,3)
		ancho=round(ancho/13.42,3)
		self.Tabla_General.insert('',0,values=(largo,ancho,peso,descripcion,categoria))

	def informacionAutor(self):
		msgI.showinfo("about Autor","Desarrollado por el Bachiller en Ingenieria" 
			"\nde Sistemas Jaime Navarro Cruz, egresado de\n"
			"la universidad Nacional José Maria Arguedas")
	#ayuda o informacion del software...
	def informacionSoftware(self):
		msgI.showinfo("about software","El Aplicativo se desarrolló con herramientas open\n"
										"source teniendo las siguientes caracteristicas:\n"
										"Lenguaje: Python v3.x\n"
										"Libreria: Opencv2\n"
										"Libreria: Numpy\n"
										"Libreria: PIL,tkinter\n"
										"version del software: v1.1\n")
	def ejecutar(self):		
		self.ventana.mainloop()

if __name__ == '__main__':
	ventana=VMain()
	ventana.ejecutar()
	
		
