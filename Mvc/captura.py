import cv2
import numpy as np
from matplotlib import pyplot as plt

"""cap=cv2.VideoCapture(1,cv2.CAP_DSHOW)
#cap.set(3,1920)
#cap.set(4,1080)

while True:
	ret,frame=cap.read()
	cv2.imshow('imagen',frame)
	valor=cv2.waitKey(1)
	if valor & 0xFF == ord('s'):
		cv2.imwrite('image/image56.png',frame)
	if valor==27:
		break
		cv2.destroyAllWindows()
cap.release()"""

img = cv2.imread('image/image20.png')

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

mask_white=cv2.inRange(res,lower_white,upper_white)

mask_black=cv2.inRange(res,lower_black,upper_black)

mask_green=cv2.inRange(res,lower_color,upper_color)

kernel=np.ones((5,5),np.uint8)
dilatado=cv2.dilate(mask_green,kernel,iterations=1)
erosionado=cv2.erode(dilatado,kernel,iterations=1)
(contorno,jerarquia)=cv2.findContours(dilatado,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cantidad=0
for c in contorno:
	if cv2.contourArea(c)>100:
		cantidad+=cv2.contourArea(c)
		cv2.drawContours(adjusted,c,-1, (0,255,0),1)
print(cantidad)



cv2.imshow('imagen valida',erosionado)
cv2.waitKey()