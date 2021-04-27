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
		self.frame=cv2.rectangle(self.frame,(20,40),(100,120),(255,2,0),2)
		self.image=Image.fromarray(self.frame)
		self.image=ImageTk.PhotoImage(self.image)
							
		return self.image
	def terminar(self):
		self.camara.release()
		self.frame=None
	
		
		





		

