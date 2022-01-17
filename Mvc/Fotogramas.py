import cv2
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox as msgI
class camara:
	camara=None
	frame=None
	image=None
	def __init__(self):
		pass

	def lectura(self,matrix):
		self.frame=cv2.cvtColor(matrix,cv2.COLOR_BGR2RGB)		
		self.image=Image.fromarray(self.frame)
		self.image=ImageTk.PhotoImage(self.image)							
		return self.image
	def detect_edge(self,img,umbral_max,umbral_min):
		img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		img=cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)
		#aplicando canny
		img_canny=cv2.Canny(img,umbral_min,umbral_max)
		return img_canny
	def terminar(self):
		self.camara.release()
		self.frame=None
	
		
		





		

