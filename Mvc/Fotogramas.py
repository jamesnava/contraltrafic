import cv2
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox as msgI
import numpy as np
import sys
import joblib
from matplotlib import pyplot as plt
class camara:
	
	def __init__(self):
		self.contorno=None

	def lectura(self,matrix):
		self.frame=cv2.cvtColor(matrix,cv2.COLOR_BGR2RGB)		
		self.image=Image.fromarray(self.frame)
		self.image=ImageTk.PhotoImage(self.image)							
		return self.image
	def formato_Tkinter(self,matrix):
		image=Image.fromarray(matrix)
		image=ImageTk.PhotoImage(image)							
		return image
	def redimensionar_image(self,imagen):
		img=cv2.resize(imagen,(int(imagen.shape[1]*0.5),int(imagen.shape[0]*0.5)),interpolation=cv2.INTER_AREA)
		return img
	def desenfoque(self,img):		
		img=cv2.GaussianBlur(img,(5,5),0)		
		return img
	def detected_edges(self,img):		
		#binarizando
		(T,thread)=cv2.threshold(img,30,255,cv2.THRESH_BINARY_INV)
		(T1,thread1)=cv2.threshold(img,65,255,cv2.THRESH_BINARY_INV)
		#realizar el bitwi
		imagen_final=cv2.bitwise_or(thread,thread1)
		#dilatacion
		kernel=np.ones((5,5),np.uint8)
		dilatado=cv2.dilate(imagen_final,kernel,iterations=2)
		#detectando contorno
		imagen_contorno=dilatado-cv2.erode(dilatado,kernel,iterations=1)
		return imagen_contorno
	def encontrar_contorno(self,imgBinary,):
		(self.contorno,jerarquia)=cv2.findContours(imgBinary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		font=cv2.FONT_HERSHEY_SIMPLEX		
		for c in self.contorno:			
			rect=cv2.minAreaRect(c)
			box=cv2.boxPoints(rect)
			#normalizamos
			box=np.int0(box)
			#hallando alturas
			lado1=((box[0][0]-box[1][0])**2+(box[0][1]-box[1][1])**2)**0.5
			lado2=((box[1][0]-box[2][0])**2+(box[1][1]-box[2][1])**2)**0.5
			lado1=round(lado1)
			lado2=round(lado2)
			largo=0
			ancho=0				
			#largo y el ancho
			if lado2<=lado1:
				largo=lado1
				ancho=lado2 
			else:
				largo=lado2
				ancho=lado1			
		return largo,ancho,box
	def dibujar_delimitador(self,img,box,largo,ancho):
		cv2.line(img,(box[0][0],box[0][1]),(box[1][0],box[1][1]),(255,255,255),1)
		cv2.line(img,(box[1][0],box[1][1]),(box[2][0],box[2][1]),(255,255,255),1)
		cv2.line(img,(box[2][0],box[2][1]),(box[3][0],box[3][1]),(255,255,255),1)
		cv2.line(img,(box[3][0],box[3][1]),(box[0][0],box[0][1]),(255,255,255),1)
		#ubicando el centro de masa			
		return img
	def analisis_Color(self,img):
		#image=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		img_copy=img.copy()
		binarizado,area_total=self.binarizacion_total(img_copy)	

		'''lower_color=np.array([40,0,0])
		upper_color=np.array([85,255,255])
		img_yuv=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
		img_yuv[:,:,0]=cv2.equalizeHist(img_yuv[:,:,0])
		img=cv2.cvtColor(img_yuv,cv2.COLOR_YUV2BGR)
		adjusted = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
		image=cv2.cvtColor(adjusted,cv2.COLOR_BGR2HSV)
		#mascara
		mask=cv2.inRange(image,lower_color,upper_color)
		image_bit=cv2.bitwise_and(image,image,mask=mask)'''
		image_binary_green,area_parcial=self.optener_masqueraGreen(img)

		#area total
	

		return image_binary_green,area_total,area_parcial

	#estimacion de los pesos de la palta
	def Prediccion_peso(self,largo,ancho):
		modelo=joblib.load('modelo.joblib')
		peso=modelo.predict([[largo,ancho]])
		return peso
	def binarizacion_total(self,img):
		gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		gray_image_des=self.desenfoque(gray_image)
		(T,thread)=cv2.threshold(gray_image_des,30,255,cv2.THRESH_BINARY_INV)
		(T1,thread1)=cv2.threshold(gray_image_des,150,255,cv2.THRESH_BINARY_INV)
		imagen_binary=cv2.bitwise_or(thread,thread1)
		kernel=np.ones((5,5),np.uint8)
		dilatado=cv2.dilate(imagen_binary,kernel,iterations=1)
		imagenPalta=cv2.erode(dilatado,kernel,iterations=2)
		area_total=self.area_(imagenPalta)
		return imagenPalta,area_total
	def optener_masqueraGreen(self,img):
		img_yuv=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
		img_yuv[:,:,0]=cv2.equalizeHist(img_yuv[:,:,0])
		img=cv2.cvtColor(img_yuv,cv2.COLOR_YUV2BGR)
		adjusted = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
		#image=cv2.cvtColor(adjusted,cv2.COLOR_BGR2HSV)
		img1=cv2.cvtColor(adjusted,cv2.COLOR_BGR2GRAY)
		img_gauss=cv2.GaussianBlur(img1,(5,5),0)
		#(T,thread)=cv2.threshold(img_gauss,50,255,cv2.THRESH_BINARY_INV)
		(T,thread2)=cv2.threshold(img_gauss,94,255,cv2.THRESH_BINARY_INV)
		res=cv2.bitwise_and(img,img,mask=thread2)
		res=cv2.cvtColor(res,cv2.COLOR_BGR2HSV)
		#verde
		lower_color=np.array([40,0,0])
		upper_color=np.array([85,255,255])
		mask_green=cv2.inRange(res,lower_color,upper_color)
		kernel=np.ones((5,5),np.uint8)
		dilatado=cv2.dilate(mask_green,kernel,iterations=1)
		#erosionado=cv2.erode(dilatado,kernel,iterations=1)
		area=self.area_verde(dilatado)
		return dilatado,area
	def area_(self,binarizado):
		(contorno,jerarquia)=cv2.findContours(binarizado,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		area=0
		for c in contorno:
			if cv2.contourArea(c)>100:
				area+=cv2.contourArea(c)			
		return area
	def area_verde(self, binarizado):
		(contorno,jerarquia)=cv2.findContours(binarizado,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		cantidad=0
		for c in contorno:			
			cantidad+=cv2.contourArea(c)
				#cv2.drawContours(adjusted,c,-1, (0,255,0),1)
		return cantidad

	def terminar(self):
		self.camara.release()
		self.frame=None

	
		
		





		

