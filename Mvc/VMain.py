import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk
import cv2
import threading 
import time
import tkinter.messagebox as msgI
#clases...
import Fotogramas
import Report
#find camera
import findCamera

class VMain:	
	
	scale_max=None
	scale_min=None
	valor_maximo_escala=None
	valor_minimo_escala=None
	#aperturar camara...
	objVideo=None
	hilo=[False]	
	#manejadorhilo
	manejador=None
	# direccion del video abierto
	Address_video=None	
	selectCamara=None
	
	#camara...
	cap=None
	def __init__(self):
		self.numeroCamara=None
		#creando objetos
		self.obj_Camera=findCamera.BuscarCamara()

		#imagenes procesar
		self.img_main=None
		self.controlador_video=0

		#configuracion basica de la ventana
		self.ventana=tk.Tk()
		self.ventana.title("SISTEMA DE CLASIFICACION DE LA PALTA")
		self.ventana.geometry('1300x650+0+10')
		#self.ventana.overrideredirect(1)
		self.ventana.protocol("WM_DELETE_WINDOW",lambda:self.EventoMSalir(self.cap))
		self.ventana.iconbitmap('../images/favicon.ico')
		self.ventana.resizable(0,0)
		self.ventana.configure(bg="#DDFFDD")
		#agregando marco izquierda
		self.Marco=tk.Frame(self.ventana,width=130,height=650)
		self.Marco.place(x=0,y=0)		
		self.Marco.config(bg="lightblue")
		self.Marco.config(relief='ridge')
		self.Marco.config(bd=3)

		#insertando los botones...
		#titulo1 del menu izquierdo...
		self.etiquetaTitulo1=tk.Label(self.Marco,text="Imágenes")
		self.etiquetaTitulo1.configure(fg="#fff",bg="#BF4262",font=("Helvetica",14,"bold","italic"),width=11,height=1,bd=2,relief="groove")
		self.etiquetaTitulo1.place(x=0,y=20)
		#Abrir y cargar imagenes...
		
		self.openVideo=tk.Button(self.Marco,text="Buscar",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.openVideo.configure(command=lambda:self.abrirDireccion(self.hilo),bd=5,overrelief="raised",width=9)
		self.openVideo.place(x=5,y=60)
		
		self.reproducirO=tk.Button(self.Marco,text="Cargar",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.reproducirO.configure(command=self.abrirImagen,bd=5,overrelief="raised")
		self.reproducirO.configure(width=9)
		self.reproducirO.place(x=5,y=160)
		#agregar separador...
		#estilo del separador...
		
		separador1Left=ttk.Separator(self.Marco,orient="horizontal")
		separador1Left.place(x=0,y=255,relwidth=5)
		#titulo2
		self.etiquetaTitulo2=tk.Label(self.Marco,text="En Vivo")
		self.etiquetaTitulo2.configure(fg="#fff",bg="#BF4262",font=("Helvetica",14,"bold","italic"),width=11,height=1,bd=2,relief="groove")
		self.etiquetaTitulo2.place(x=0,y=255)

		self.Bconfigurar=tk.Button(self.Marco,text="Selec. Cam.",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.Bconfigurar.configure(width=9)
		self.Bconfigurar.configure(command=self.obj_Camera.Top_Camera,bd=5,overrelief="raised")
		self.Bconfigurar.place(x=5,y=300)

		#play
		self.BIniciar=tk.Button(self.Marco,text="Iniciar",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.BIniciar.configure(width=9,command=self.EventBIVideo,bd=5,overrelief="raised")
		self.BIniciar.place(x=5,y=395)

		separador2Left=ttk.Separator(self.Marco,orient="horizontal")
		separador2Left.place(x=0,y=490,relwidth=10)

		self.BTerminar=tk.Button(self.Marco,text="Detener",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.BTerminar.configure(command=lambda:self.EventBTVideo(self.hilo),bd=5,overrelief="raised")
		self.BTerminar.configure(width=9)
		self.BTerminar.place(x=5,y=510)

		separador3Left=ttk.Separator(self.Marco,orient="horizontal")

		separador3Left.place(x=0,y=610,relwidth=5)

		#fin de izquierdo
		#agregando marco principal
		self.MarcoP=tk.Frame(self.ventana,width=1150,height=570)
		self.MarcoP.config(relief='ridge')
		self.MarcoP.config(bd=3)
		self.MarcoP.place(x=130,y=0)
		#Label video
		etiqueta_titulo_cuadro1=tk.Label(self.MarcoP,text="Imagen Original")
		etiqueta_titulo_cuadro1.place(x=22,y=3)
		self.EtiquetaVideo=tk.Label(self.MarcoP,text="Imagen1",font=('Times',14,"bold","italic"),bg="#232928",fg="#fff",bd=5,relief="sunken")

		self.EtiquetaVideo.config(width="30",height="10")
		
		self.EtiquetaVideo.place(x=20,y=10)
		
		#etiqueta imagen binarizada
		etiqueta_titulo_cuadro2=tk.Label(self.MarcoP,text="Imagen2")
		etiqueta_titulo_cuadro2.place(x=395,y=3)
		self.EtiquetaIBinarizada=tk.Label(self.MarcoP,text="Imagen 2",font=('Times',14,"bold","italic"),bg="#232928",fg="#fff",relief="sunken")
		self.EtiquetaIBinarizada.config(width="30",height="10")
		self.EtiquetaIBinarizada.place(x=390,y=5)

		#etiqueta 3ra imagen
		etiqueta_titulo_cuadro3=tk.Label(self.MarcoP,text="Imagen Original")
		etiqueta_titulo_cuadro3.place(x=775,y=3)
		self.EtiquetaImagen3=tk.Label(self.MarcoP,text="Imagen 2",font=('Times',14,"bold","italic"),bg="#232928",fg="#fff",relief="sunken")
		self.EtiquetaImagen3.config(width="30",height="10")
		self.EtiquetaImagen3.place(x=770,y=5)

		#agragar escalas
		
		etiquetaEscala=tk.Label(self.MarcoP,text="Umbral para la deteccion de Bordes",font=('times',11,'bold','italic'))
		
		etiquetaEscala.place(x=20,y=245)
		self.scale_max=tk.Scale(self.MarcoP,from_=0,to=256,orient='horizontal',length=150,label="Max")
		
		self.scale_max.place(x=200,y=280)

		self.scale_min=tk.Scale(self.MarcoP,from_=0,to=256,orient='horizontal',length=150,label="Min")
		self.scale_min.place(x=20,y=280)

		btn_process=tk.Button(self.MarcoP,text='Procesar')
		btn_process.config(command=self.deteccion_bordes)
		btn_process.place(x=400,y=280)

		#marco bottom
		self.MarcoBottom=tk.Frame(self.ventana,width=1150,height=80)
		#self.MarcoBottom.pack(side="bottom")
		#self.MarcoBottom.pack_propagate(False)
		self.MarcoBottom.config(bg="#D1CBC7")
		self.MarcoBottom.config(relief='ridge')
		self.MarcoBottom.config(bd=3)
		self.MarcoBottom.place(x=130,y=575)
			
		
		#cantidad de tiempo
		self.segundo=tk.Label(self.MarcoBottom,text="0",font=('Courier',14),width=4)
		self.segundo.place(x=5,y=0)

		self.minuto=tk.Label(self.MarcoBottom,text="0",font=('Courier',14),width=4)
		#self.minuto.pack(side="right",padx=2)

		self.hora=tk.Label(self.MarcoBottom,text="0",font=('Courier',14),width=4)
		#self.hora.pack(side="right",padx=5)

		self.EtiquetaTiempo=tk.Label(self.MarcoBottom,text="Tiempo :",font=('Courier',14,"bold","italic"))
		#self.EtiquetaTiempo.pack(side="right",padx=1)
		self.BarraMenu()
		#hilo
		
		#inicializar la camara...	
	def BarraMenu(self):
		self.BarraMenu=tk.Menu(self.ventana)
		self.ventana.config(menu=self.BarraMenu)
		#creando submenues Ayuda.
		AyudaM=tk.Menu(self.BarraMenu,tearoff=0)
		AyudaM.add_command(label="Autor",command=self.informacionAutor)
		AyudaM.add_command(label="Acerca de...",command= self.informacionSoftware)
		#menú configuracion...
		ConfiguracionM=tk.Menu(self.BarraMenu,tearoff=0)
		#ConfiguracionM.add_command(label="seleccionar Camara",command=self.FindCamera)
		ConfiguracionM.add_command(label="Cargar Video",command=lambda:self.abrirDireccion(self.hilo))
		ConfiguracionM.add_command(label="Minimizar",command=lambda :self.ventana.iconify())
		ConfiguracionM.add_command(label="Salir",command=lambda:self.EventoMSalir(self.cap))
		#menu operaciones
		Reportes=tk.Menu(self.BarraMenu,tearoff=0)
		Reportes.add_command(label="Reporte")
		Reportes.add_command(label="Exportar a PDF")
		#agregando los menues...
		self.BarraMenu.add_cascade(label="Configuracion",menu=ConfiguracionM)
		self.BarraMenu.add_cascade(label="Acciones",menu=Reportes)
		self.BarraMenu.add_cascade(label="Ayuda",menu=AyudaM)	
		
	def AbrirFotogramas(self,mirror=False):
		if self.numeroCamara!=None:				
			self.cap=cv2.VideoCapture(int(self.numeroCamara),cv2.CAP_DSHOW)			
			self.objVideo=Fotogramas.camara()
			ss=0
			hh=0
			mm=0
			segundosF=0	
			self.CantidadTiempo=0				
			while True:
				ret,FrameMatriz=self.cap.read()
				if mirror is True:
					FrameMatriz=FrameMatriz[:,::-1]
				
				fotograma=self.objVideo.lectura(FrameMatriz)
				self.EtiquetaVideo.config(width="330",height="215")
				self.EtiquetaVideo.configure(image=fotograma)
				self.EtiquetaVideo.image=fotograma
				segundosF=segundosF+1
				if segundosF==30:
					ss=ss+1
					self.CantidadTiempo=self.CantidadTiempo+1
					segundosF=0					
				if ss==60:
					ss=0
					mm=mm+1					
				if mm==60:
					hh=hh+1
					mm=0
					
				self.segundo.configure(text=str(ss))
				self.minuto.configure(text=str(mm))
				self.hora.configure(text=str(hh))

				if self.hilo[0]:
					self.hilo[0]=False
					self.EtiquetaVideo.configure(image='')
					self.EtiquetaVideo.configure(text='Imagen 1')
					self.EtiquetaVideo.config(width="30",height="10")
					break
			self.cap.release()
			self.cap=None
				
		else:
			msgI.showinfo("Alerta!!","Seleccione Camara!!")
	def EventBIVideo(self):
		self.numeroCamara=self.obj_Camera.numeroCamera		
		self.manejador=threading.Thread(target=self.AbrirFotogramas)
		self.manejador.start()	
	def EventBTVideo(self,hilo):		
		hilo[0]=True			
	def EventoMSalir(self,cap):
		if cap==None:
			self.ventana.destroy()
		else:
			msgI.showinfo("Alerta!","Antes Presione el Boton Parar!!")	
	def abrirDireccion(self,hilo):
		hilo[0]=True
		self.Address_video=filedialog.askopenfilename()		
	def abrirImagen(self):
		if self.Address_video!=None:
			self.objVideo=Fotogramas.camara()
			img_source=cv2.imread(self.Address_video)
			self.img_main=img_source
			img_source=cv2.resize(img_source,(330,215),interpolation=cv2.INTER_AREA)
			img_source=self.objVideo.lectura(img_source)
			self.EtiquetaVideo.config(width="330",height="215")
			self.EtiquetaVideo.configure(image=img_source)
			self.EtiquetaVideo.image=img_source
		self.objVideo=None
					
	def deteccion_bordes(self):
		
		if self.objVideo==None:
			self.objVideo=Fotogramas.camara()
			img_with_edge=self.objVideo.detect_edge(self.img_main,self.scale_max.get(),self.scale_min.get())
			img_with_edge=cv2.resize(img_with_edge,(330,215),interpolation=cv2.INTER_AREA)
			img_with_edge=self.objVideo.lectura(img_with_edge)

			self.EtiquetaIBinarizada.config(width="330",height="215")
			self.EtiquetaIBinarizada.configure(image=img_with_edge)
			self.EtiquetaIBinarizada.image=img_with_edge
		else:
			img_with_edge=self.objVideo.detect_edge(self.img_main,self.scale_max.get(),self.scale_min.get())
			img_with_edge=cv2.resize(img_with_edge,(330,215),interpolation=cv2.INTER_AREA)
			img_with_edge=self.objVideo.lectura(img_with_edge)

			self.EtiquetaIBinarizada.config(width="330",height="215")
			self.EtiquetaIBinarizada.configure(image=img_with_edge)
			self.EtiquetaIBinarizada.image=img_with_edge

			


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
	
		
