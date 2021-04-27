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
	ventana=None
	BarraMenu=None
	#marcos
	MarcoP=None
	Marco=None
	MarcoBottom=None
	#botones
	Bconfigurar=None
	BTerminar=None
	BIniciar=None
	openVideo=None
	reproducirO=None
	#etiquetas
	EtiquetaCamion=None
	EtiquetaMototaxi=None
	EtiquetaAutos=None
	#etiqueta video contenedor...
	EtiquetaVideo=None
	#etiqueta que almacena la cantidad de objetos...
	CantidadCamion=None
	CantidadMototaxi=None
	CantidadAutos=None
		#etiqueta tiempo
	EtiquetaTiempo=None
	CantidadTiempo=0
	hora=None
	minuto=None
	segundo=None
	#aperturar camara...
	objVideo=None
	hilo=[False]	
	#manejadorhilo
	manejador=None
	# direccion del video abierto
	Address_video=None
	#toplevels
	#buscador de camaras...
	top1=None
	#componentes de toplevels...
	#componente del primer top...
	selectCamara=None
	numeroCamara=None
	#camara...
	cap=None
	#etiquetas menu izquierdo...
	etiquetaTitulo1=None
	etiquetaTitulo2=None

	def __init__(self):
		#configuracion basica de la ventana
		self.ventana=tk.Tk()
		self.ventana.title("SISTEMA DE MONITOREO DE TRAFICO VEHICULAR EN TIEMPO REAL")
		self.ventana.geometry('1300x650+0+10')
		#self.ventana.overrideredirect(1)
		self.ventana.protocol("WM_DELETE_WINDOW",lambda:self.EventoMSalir(self.cap))
		self.ventana.iconbitmap('../images/favicon.ico')
		self.ventana.resizable(0,0)
		self.ventana.configure(bg="#DDFFDD")
		#agregando marco izquierda
		self.Marco=tk.Frame(self.ventana,width=130,height=650)
		self.Marco.pack(side="left")
		self.Marco.pack_propagate(False)
		self.Marco.config(bg="lightblue")
		self.Marco.config(relief='ridge')
		self.Marco.config(bd=3)

		#insertando los botones...
		#titulo1 del menu izquierdo...
		self.etiquetaTitulo1=tk.Label(self.Marco,text="Abrir Video")
		self.etiquetaTitulo1.configure(fg="#fff",bg="#BF4262",font=("Helvetica",14,"bold","italic"),width=11,height=1,bd=2,relief="groove")
		self.etiquetaTitulo1.place(x=0,y=20)
		#open video...
		
		self.openVideo=tk.Button(self.Marco,text="Direccionar",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.openVideo.configure(command=lambda:self.abrirDireccion(self.hilo),bd=5,overrelief="raised",width=9)
		self.openVideo.place(x=5,y=60)

		#
		self.reproducirO=tk.Button(self.Marco,text="Reproducir",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.reproducirO.configure(command=lambda:self.eventBAVideo(self.hilo),bd=5,overrelief="raised")
		self.reproducirO.configure(width=9)
		self.reproducirO.place(x=5,y=160)


		#agregar separador...
		#estilo del separador...
		
		separador1Left=ttk.Separator(self.Marco,orient="horizontal")
		separador1Left.place(x=0,y=255,relwidth=5)
		#titulo2
		self.etiquetaTitulo2=tk.Label(self.Marco,text="Streaming")
		self.etiquetaTitulo2.configure(fg="#fff",bg="#BF4262",font=("Helvetica",14,"bold","italic"),width=11,height=1,bd=2,relief="groove")
		self.etiquetaTitulo2.place(x=0,y=255)

		self.Bconfigurar=tk.Button(self.Marco,text="Buscar Cam.",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.Bconfigurar.configure(width=9)
		self.Bconfigurar.configure(command=self.FindCamera,bd=5,overrelief="raised")
		self.Bconfigurar.place(x=5,y=300)

		#play
		self.BIniciar=tk.Button(self.Marco,text="Iniciar",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.BIniciar.configure(width=9,command=lambda:self.EventBIVideo(self.hilo),bd=5,overrelief="raised")
		self.BIniciar.place(x=5,y=395)

		separador2Left=ttk.Separator(self.Marco,orient="horizontal")
		separador2Left.place(x=0,y=490,relwidth=10)

		self.BTerminar=tk.Button(self.Marco,text="Parar",fg="#fff",bg="#232928",font=("",14),height=3,cursor="hand2")
		self.BTerminar.configure(command=lambda:self.EventBTVideo(self.hilo),bd=5,overrelief="raised")
		self.BTerminar.configure(width=9)
		self.BTerminar.place(x=5,y=510)

		separador3Left=ttk.Separator(self.Marco,orient="horizontal")

		separador3Left.place(x=0,y=610,relwidth=5)

		#fin de izquierdo
		#agregando marco principal
		self.MarcoP=tk.Frame(self.ventana,width=1150,height=570)
		self.MarcoP.pack()

		self.MarcoP.pack_propagate(False)
		self.MarcoP.config(relief='ridge')
		self.MarcoP.config(bd=3)
		#Label video
		self.EtiquetaVideo=tk.Label(self.MarcoP,text="PANTALLA PRINCIPAL",font=('Times',28,"bold","italic"),bg="#232928",fg="#fff",bd=20,relief="sunken")

		self.EtiquetaVideo.config(width="1000",height="570")
		self.EtiquetaVideo.pack(padx=5,pady=5)
		#marco bottom
		self.MarcoBottom=tk.Frame(self.ventana,width=1150,height=80)
		self.MarcoBottom.pack(side="bottom")
		self.MarcoBottom.pack_propagate(False)
		self.MarcoBottom.config(bg="#D1CBC7")
		self.MarcoBottom.config(relief='ridge')
		self.MarcoBottom.config(bd=3)
			#agragar Label...
		self.EtiquetaAutos=tk.Label(self.MarcoBottom,text="Autos :",font=('Courier',14,"bold","italic"))
		self.EtiquetaAutos.pack(side="left",padx=5)

		#cantidad de autos
		self.CantidadAutos=tk.Label(self.MarcoBottom,text="10",font=('Courier',14))
		self.CantidadAutos.pack(side="left",padx=5)
		#etiqueta mototaxi
		self.EtiquetaMototaxi=tk.Label(self.MarcoBottom,text="Mototaxi :",font=('Courier',14,"bold","italic"))
		self.EtiquetaMototaxi.pack(side="left",padx=10)

		#cantidad de Mototaxis
		self.CantidadMototaxi=tk.Label(self.MarcoBottom,text="30",font=('Courier',14))
		self.CantidadMototaxi.pack(side="left",padx=5)

		#etiqueta camiones...
		self.EtiquetaCamion=tk.Label(self.MarcoBottom,text="Camiones :",font=('Courier',14,"bold","italic"))
		self.EtiquetaCamion.pack(side="left",padx=10)
		#cantidad de camiones
		self.CantidadCamion=tk.Label(self.MarcoBottom,text="50",font=('Courier',14))
		self.CantidadCamion.pack(side="left",padx=5)
		#tiempo
		#cantidad de tiempo
		self.segundo=tk.Label(self.MarcoBottom,text="0",font=('Courier',14),width=4)
		self.segundo.pack(side="right",padx=2)

		self.minuto=tk.Label(self.MarcoBottom,text="0",font=('Courier',14),width=4)
		self.minuto.pack(side="right",padx=2)

		self.hora=tk.Label(self.MarcoBottom,text="0",font=('Courier',14),width=4)
		self.hora.pack(side="right",padx=5)

		self.EtiquetaTiempo=tk.Label(self.MarcoBottom,text="Tiempo :",font=('Courier',14,"bold","italic"))
		self.EtiquetaTiempo.pack(side="right",padx=1)
		
		#agregando menu


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
		ConfiguracionM.add_command(label="seleccionar Camara",command=self.FindCamera)
		ConfiguracionM.add_command(label="Cargar Video",command=lambda:self.abrirDireccion(self.hilo))
		ConfiguracionM.add_command(label="Minimizar",command=self.EventoMMinimizar)
		ConfiguracionM.add_command(label="Salir",command=lambda:self.EventoMSalir(self.cap))
		#menu operaciones
		Reportes=tk.Menu(self.BarraMenu,tearoff=0)
		Reportes.add_command(label="Reporte",command=lambda:self.eventoReporte(self.ventana))
		Reportes.add_command(label="Exportar a PDF")
		#agregando los menues...
		self.BarraMenu.add_cascade(label="Configuracion",menu=ConfiguracionM)
		self.BarraMenu.add_cascade(label="Acciones",menu=Reportes)
		self.BarraMenu.add_cascade(label="Ayuda",menu=AyudaM)
	def FindCamera(self):
		'''self.ventana.wm_attributes("-disabled",1)
		objFindCamera=findCamera.BuscarCamara()
		objFindCamera.ejecutarVentana()'''
		self.top1 = tk.Toplevel(self.ventana, bg="Orange",relief="groove")
		self.top1.title("Seeleccionar Cámara")
		self.top1.geometry("500x170+200+120")
		self.top1.overrideredirect(1)
		self.top1.wm_attributes("-topmost",1)
		self.top1.resizable(0,0)

		labelCamara=tk.Label(self.top1,text="Seleccione una Cámara:")
		labelCamara.configure(width=20,bg="Orange",font=("",14),height=3)
		labelCamara.place(x=0,y=20)

		#agregando un select...
		self.selectCamara=ttk.Combobox(self.top1,font=("",14),height=3)
		self.selectCamara["values"]=[0,1,2,3,4,5,6,7,8,9]
		self.selectCamara.current(0)
		self.selectCamara.place(x=250,y=40)
		#agregando un boton...
		botonAceptar=tk.Button(self.top1,text="Aceptar",bg="#FFF",font=("",14))
		botonAceptar.configure(width=9,command=self.AceptarFindCamera)
		botonAceptar.place(x=160,y=100)
		 
		self.ventana.wm_attributes("-disabled",1)
	def AceptarFindCamera(self):
		self.numeroCamara=self.selectCamara.get()	
		self.top1.destroy()
		self.top1=None
		self.ventana.wm_attributes("-disabled",0)
	def AbrirFotogramas(self,mirror=False):
		if self.numeroCamara!=None:				
			self.cap=cv2.VideoCapture(int(self.numeroCamara))
			self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
			self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,570)
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
					self.EtiquetaVideo.configure(text='PANTALLA PRINCIPAL')
					break
			self.cap.release()
			self.cap=None
				
		else:
			msgI.showinfo("Alerta!!","Seleccione Camara!!")
	def EventBIVideo(self,hilo):		
		self.manejador=threading.Thread(target=self.AbrirFotogramas,args=(hilo,))
		self.manejador.start()		
	def EventBTVideo(self,hilo):
		hilo[0]=True			
	def EventoMSalir(self,cap):
		if cap==None:
			self.ventana.destroy()
		else:
			msgI.showinfo("Alerta!","Antes Presione el Boton Parar!!")		
	def EventoMMinimizar(self):
		self.ventana.iconify()
	def abrirDireccion(self,hilo):
		hilo[0]=True
		self.Address_video=filedialog.askopenfilename()		
	def abrirVideo(self,mirror=False):
		if self.Address_video!=None:
			direccion=self.Address_video
			self.cap=cv2.VideoCapture(direccion)	
			self.objVideo=Fotogramas.camara()
			ss=0
			hh=0
			mm=0
			segundosF=0	
			self.CantidadTiempo=0	
			while True:
				ret,frame=self.cap.read()
				if mirror is True:
					frame=frame[:,::-1]
				if ret:
					fotograma=self.objVideo.lectura(frame)
					self.EtiquetaVideo.configure(image=fotograma)
					self.EtiquetaVideo.image=fotograma
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

					time.sleep(0.027)
					if self.hilo[0]:
						self.hilo[0]=False
						self.EtiquetaVideo.configure(image='')
						self.EtiquetaVideo.configure(text='PANTALLA PRINCIPAL')
						break
				else:
					self.hilo[0]=False
					self.EtiquetaVideo.configure(image='')
					self.EtiquetaVideo.configure(text='PANTALLA PRINCIPAL')
					break
			self.cap.release()
			self.cap=None
		else:
			msgI.showinfo("Alerta!!","seleccione un video!!")			
	def eventBAVideo(self,hilo):
		self.manejador=threading.Thread(target=self.abrirVideo,args=(hilo,))
		self.manejador.start()
	def eventoReporte(self,ventana):
		cantidadMoto=self.CantidadMototaxi.cget("text")
		cantidadCamio=self.CantidadCamion.cget("text")
		cantidadAuto=self.CantidadMototaxi.cget("text")
		cantidadDeTiempo=self.CantidadTiempo
		
		objReporte=Report.Reports(ventana,cantidadMoto,cantidadCamio,cantidadAuto,cantidadDeTiempo)
	#acerca del autor...
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
	
		
