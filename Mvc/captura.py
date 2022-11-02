import cv2
import numpy as np
from matplotlib import pyplot as plt

'''cap=cv2.VideoCapture(1,cv2.CAP_DSHOW)
#cap.set(3,1920)
#cap.set(4,1080)

while True:
	ret,frame=cap.read()
	cv2.imshow('imagen',frame)
	valor=cv2.waitKey(1)
	if valor & 0xFF == ord('s'):
		cv2.imwrite('image/imageE20.png',frame)
	if valor==27:
		break
		cv2.destroyAllWindows()
cap.release()'''
img = cv2.imread('image/image20.png')
img1=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#img_rg=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#img_yuv=cv2.cvtColor(img_rg,cv2.COLOR_BGR2YUV)
#img_yuv[:,:,0]=cv2.equalizeHist(img_yuv[:,:,0])
#img=cv2.cvtColor(img_yuv,cv2.COLOR_YUV2BGR)
#adjusted = cv2.convertScaleAbs(img, alpha=1.5, beta=0)

'''img2=cv2.cvtColor(adjusted,cv2.COLOR_BGR2HSV)
lower_green=np.array([40,0,0])
upper_green=np.array([70,255,255])
mask=cv2.inRange(img2,lower_green,upper_green)
res=cv2.bitwise_and(img2,img2,mask=mask)
hist=cv2.calcHist([res],[0],None,[256],[0,256])'''

#res=cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
img_gauss=cv2.GaussianBlur(img1,(5,5),0)	
#hist=cv2.calcHist([img_gauss],[0],None,[256],[0,256])
#plt.plot(hist,color='gray')
#plt.show()
#(T,thread)=cv2.threshold(img_gauss,50,255,cv2.THRESH_BINARY_INV)
(T,thread2)=cv2.threshold(img_gauss,94,255,cv2.THRESH_BINARY_INV)
res=cv2.bitwise_and(img,img,mask=thread2)
res=cv2.cvtColor(res,cv2.COLOR_BGR2HSV)
hist=cv2.calcHist([res],[0],None,[256],[0,256])
plt.plot(hist,color='gray')
plt.show()
#imagen_final=cv2.bitwise_and(thread,thread2)
#ecualizado=cv2.equalizeHist(img2)
#ecualizado1=cv2.cvtColor(ecualizado,cv2.COLOR_GRAY2BGR)
lower_black=np.array([105,100,0])
upper_black=np.array([110,255,255])

#la parte blanca
lower_white=np.array([0,0,0])
upper_white=np.array([10,255,255])

mask_white=cv2.inRange(res,lower_white,upper_white)

mask_black=cv2.inRange(res,lower_black,upper_black)




cv2.imshow('desperfectos blancos',mask_white)
cv2.imshow('desperfectos negros',mask_black)
cv2.imshow('analizado',res)
cv2.waitKey()