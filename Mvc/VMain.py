import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2
import numpy as np
import threading 
import tkinter.messagebox as msgI
from matplotlib import pyplot as plt
#clases...
import Fotogramas
import Report
import findCamera

class VMain(object):	
	objVideo=None	
	def __init__(self):
		self.numeroCamara=None
		self.hilo=False
		self.matriz_Image=None
		self.cap=None
		#creando objetos
		self.obj_Camera=findCamera.BuscarCamara()
		self.objVideo=Fotogramas.camara()	
		self.controlador_video=0
		#configuracion basica de la ventana
		self.ventana=tk.Tk()
		self.ventana.title("SISTEMA DE CLASIFICACION DE LA PALTA")
		screen_width = self.ventana.winfo_screenwidth()
		screen_height = self.ventana.winfo_screenheight()
		self.ventana.geometry(f'{int(screen_width*0.99)}x{int(screen_height*0.90)}+0+0')
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
		self.BIniciar.configure(width=9,command=self.InicioVideo,bd=5,overrelief="raised")
		self.BIniciar.place(x=5,y=395)

		separador2Left=ttk.Separator(self.Marco,orient="horizontal")
		separador2Left.place(x=0,y=490,relwidth=10)

		self.BTerminar=tk.Button(self.Marco,text="Liberar Cam.",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.BTerminar.configure(command=self.CapturaImagen,bd=5,overrelief="raised")
		self.BTerminar.configure(width=9)
		self.BTerminar.place(x=5,y=510)

		separador3Left=ttk.Separator(self.Marco,orient="horizontal")

		separador3Left.place(x=0,y=610,relwidth=5)

		#fin de izquierdo
		#agregando marco principal
		self.MarcoP=tk.Frame(self.ventana,width=int(screen_width*0.88),height=570)
		self.MarcoP.config(relief='ridge')
		self.MarcoP.config(bd=3)
		self.MarcoP.place(x=130,y=0)
		#Label video
		etiqueta_titulo_cuadro1=tk.Label(self.MarcoP,text="Imagen Original")
		etiqueta_titulo_cuadro1.place(x=22,y=1)
		self.EtiquetaVideo=tk.Label(self.MarcoP,text="Imagen original",font=('Times',14,"bold","italic"),bg="#232928",fg="#fff",bd=5,relief="sunken")
		self.EtiquetaVideo.config(width="26",height="9")	
		self.EtiquetaVideo.place(x=10,y=20)
		
		#etiqueta imagen binarizada
		etiqueta_titulo_cuadro2=tk.Label(self.MarcoP,text="Imagen2")
		etiqueta_titulo_cuadro2.place(x=395,y=1)
		self.EtiquetaIBinarizada=tk.Label(self.MarcoP,text="Imagen ",font=('Times',14,"bold","italic"),bg="#232928",fg="#fff",relief="sunken")
		self.EtiquetaIBinarizada.config(width="26",height="9")
		self.EtiquetaIBinarizada.place(x=420,y=20)

		#etiqueta 3ra imagen
		etiqueta_titulo_cuadro3=tk.Label(self.MarcoP,text="Imagen Original")
		etiqueta_titulo_cuadro3.place(x=775,y=1)
		self.EtiquetaImagen3=tk.Label(self.MarcoP,text="Imagen 2",font=('Times',14,"bold","italic"),bg="#232928",fg="#fff",relief="sunken")
		self.EtiquetaImagen3.config(width="26",height="9")
		self.EtiquetaImagen3.place(x=850,y=20)
		

		btn_process=tk.Button(self.MarcoP,text='Procesar')
		btn_process.config(command=self.deteccion_bordes)
		btn_process.place(x=400,y=280)

		#agregando la tabla
		self.Tabla_General=ttk.Treeview(self.MarcoP,columns=('#1','#2','#3','#4','5'),show='headings')
		self.Tabla_General.heading('#1',text='Ancho')
		self.Tabla_General.heading('#2',text='Largo')
		self.Tabla_General.heading('#3',text='Peso')
		self.Tabla_General.heading('#4',text='Categoria')
		self.Tabla_General.heading('#5',text='Descripcion')
		self.Tabla_General.place(x=10,y=310,width=1000,height=200)
		#marco bottom
		self.MarcoBottom=tk.Frame(self.ventana,width=int(screen_width*0.88),height=80)
		
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
		
		#agregando los menues...
		self.BarraMenu.add_cascade(label="Configuracion",menu=ConfiguracionM)
		
		self.BarraMenu.add_cascade(label="Ayuda",menu=AyudaM)	
		
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
		self.numeroCamara=self.obj_Camera.numeroCamera		
		self.manejador=threading.Thread(target=self.AbrirFotogramas)
		self.manejador.start()	
	def CapturaImagen(self):		
		self.hilo=True			
	def EventoMSalir(self,cap):
		if self.cap==None:
			self.ventana.destroy()
		else:
			msgI.showinfo("Alerta!","Antes Presione el Boton Parar!!")	
	def abrirDireccion(self,hilo):
		hilo=True
		self.Address_video=filedialog.askopenfilename()		
	def abrirImagen(self):
		if self.Address_video!=None:			
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
		img=self.matriz_Image
		img1=img				
		img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)				
		#redimensionando las imagenes
		img=self.objVideo.redimensionar_image(img)
		img1=self.objVideo.redimensionar_image(img1)

		img=self.objVideo.detected_edges(self.objVideo.desenfoque(img))
		largo,ancho,cordenadas=self.objVideo.encontrar_contorno(img)
		#prediccion del peso de la palta
		peso_palta=self.objVideo.Prediccion_peso(round(largo/13.42)*10,round(ancho/13.42)*10)		
		self.datos_Table(largo,ancho,round(peso_palta[0][0],1),'Categoria A')
		img=self.objVideo.dibujar_delimitador(img,cordenadas,largo,ancho)
		img=self.objVideo.formato_Tkinter(img)
		self.EtiquetaIBinarizada.config(width='320',height='240')
		self.EtiquetaIBinarizada.configure(image=img)
		self.EtiquetaIBinarizada.image=img

		#analisis de color
		img1=self.objVideo.analisis_Color(img1)
		img1=self.objVideo.formato_Tkinter(img1)
		self.EtiquetaImagen3.config(width='320',height='240')
		self.EtiquetaImagen3.configure(image=img1)
		self.EtiquetaImagen3.image=img1
	def datos_Table(self,largo,ancho,peso,descripcion):
		largo=round(largo/13.42)
		ancho=round(ancho/13.42)
		self.Tabla_General.insert('','end',values=(largo,ancho,peso,descripcion))

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
	
		
