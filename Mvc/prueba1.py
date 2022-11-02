import cv2 
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage



'''img=cv2.imread('image/20.jpg')
img_yuv=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
img_yuv[:,:,0]=cv2.equalizeHist(img_yuv[:,:,0])
img=cv2.cvtColor(img_yuv,cv2.COLOR_YUV2BGR)
img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#img=cv2.cvtColor(img,cv2.COLOR_HSV2GRAY)
 

lower_green=np.array([50,10,10])
upper_green=np.array([85,255,255])
mask=cv2.inRange(img,lower_green,upper_green)
res=cv2.bitwise_and(img,img,mask=mask)
cantidad=0
for i in range(mask.shape[0]):
	for j in range(mask.shape[1]):
		if mask[i][j]>0:
			cantidad+=1
cv2.imshow('res',res)
cv2.waitKey()'''

'''camara=cv2.VideoCapture(1,cv2.CAP_DSHOW)
while True:
	ret,frame=camara.read()
	#frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	lower_blue=np.array([110,100,100])
	upper_blue=np.array([130,255,255])
	mask=cv2.inRange(frame,lower_blue,upper_blue)
	res=cv2.bitwise_and(frame,frame,mask=mask)
	res=cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
	cv2.imshow('imagen',res)
	if cv2.waitKey(1)==27:
		break
camara.release()
cv2.destroyAllWindows()'''


'''img=cv2.imread('image/image01.png')
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
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
imagen_limpia=dilatado-cv2.erode(dilatado,kernel,iterations=1)
#econtrando contorno
contours, hierarchy = cv2.findContours(imagen_limpia,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
 
# Draw all contours
# -1 signifies drawing all contours
cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
  
cv2.imshow('Contours',imagen_limpia)
cv2.waitKey(0)'''
