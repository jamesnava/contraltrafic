import cv2
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox as msgI
import numpy as np
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
		img1=cv2.GaussianBlur(img,(7,7),0)
		#hist=cv2.calcHist([img],[0],None,[256],[0,256])
		#plt.plot(hist,color='b')
		#plt.show()
		#binarizando
		(T,thread)=cv2.threshold(img1,30,255,cv2.THRESH_BINARY_INV)
		(T1,thread1)=cv2.threshold(img1,65,255,cv2.THRESH_BINARY_INV)

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

		#dibujando los contornos
		#img_dibujado=cv2.drawContours(imgOriginal,self.contorno,-1,(0,255,0),2)
		
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
			#largo y el ancho
			if lado2<=lado1:
				largo=lado1 
			else:
				largo=lado2
			if lado1<=lado2:
				ancho=lado1 
			else:
				ancho=lado1
		return imgBinary,largo,ancho,box
	def dibujar_delimitador(self,img,box,largo,ancho):
		cv2.line(img,(box[0][0],box[0][1]),(box[1][0],box[1][1]),(255,255,255),1)
		cv2.line(img,(box[1][0],box[1][1]),(box[2][0],box[2][1]),(255,255,255),1)
		cv2.line(img,(box[2][0],box[2][1]),(box[3][0],box[3][1]),(255,255,255),1)
		cv2.line(img,(box[3][0],box[3][1]),(box[0][0],box[0][1]),(255,255,255),1)
		#ubicando el centro de masa
		font=cv2.FONT_HERSHEY_SIMPLEX
		#insertamos letra
		#las proporciones 1cm->13.42 pixeles
		cv2.putText(img,f'(L:{round(largo/13.42,2)},A: {round(ancho/13.42,2)})',(10,50),font,1,(255,255,255),1)
		return img
	def terminar(self):
		self.camara.release()
		self.frame=None
	
		
		





		

