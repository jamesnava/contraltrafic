
import cv2
 
cascada=cv2.CascadeClassifier('D:/cara.xml')

cap=cv2.VideoCapture(0)

ret,frame=cap.read()
font=cv2.FONT_HERSHEY_SIMPLEX
while True:
	imgM=frame.copy()
	frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	contornos=cascada.detectMultiScale(frame,1.3,5)
	for valores in contornos:
		(x,y,w,h)=valores
		cv2.rectangle(imgM,(x,y),(x+w,y+h),(255,0,0),2)
		cv2.putText(imgM,"Jaime",(x,y),font,0.5,(0,255,0),2)
	ret,frame=cap.read()

	cv2.imshow('ventana',imgM)
	if cv2.waitKey(1)==27:
		break
cv2.destroyAllWindows()
cap.release()