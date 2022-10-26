import cv2
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox as msgI
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
		img=cv2.Canny(img,100,200)
		return img
	def encontrar_contorno(self,imgCanny,imgOriginal):
		(self.contorno,jerarquia)=cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		font=cv2.FONT_HERSHEY_SIMPLEX

		#dibujando los contornos
		#img_dibujado=cv2.drawContours(imgOriginal,self.contorno,-1,(0,255,0),2)
		
		for c in self.contorno:
			x,y,w,h=cv2.boundingRect(c)
			cv2.rectangle(imgOriginal,(x,y),(x+w,y+h),(0,0,255),1)
			#reducimos 1 cm
			cv2.putText(imgOriginal,(f"""A: {round(w/12.19,2)}, L: {round(h/12.19,2)}"""),(x,y),font,0.5,(255,0,0),2)

		return imgOriginal
	def terminar(self):
		self.camara.release()
		self.frame=None
	
		
		





		

