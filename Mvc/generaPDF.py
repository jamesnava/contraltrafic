from reportlab.pdfgen import canvas as can
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image
import database
from tkinter import messagebox


class Reporte(object):
	def __init__(self):		
		pdfmetrics.registerFont(TTFont('Vera','Vera.ttf'))
		self.obj_consulta=database.database()		
	def Reporte_(self,usuario,desde,hasta,pesos,categorias):
		rows=self.obj_consulta.consultar_User(usuario)
		datos=rows[0][1]+' '+rows[0][2]
		libro=can.Canvas('Reporte.pdf',pagesize=A4)
		w,h=A4		
		libro.drawString(20,h-20,f'REPORTE GENERAL')
		libro.drawString(20,h-45,f'USUARIO: {datos}')
		libro.drawString(20,h-65,f'DESDE: {desde}')
		libro.drawString(20,h-85,f'HASTA: {hasta}')
		libro.drawString(20,h-95,'____________________________________________________________________________________')
		
		libro.drawString(305,h-120,'PESOS')
		libro.drawString(25,h-120,'CATEGORIAS')
		libro.drawString(405,h-120,'PREC. X KG')
		libro.drawString(485,h-120,'SUB TOTAL.')
		posy=h-220

		#posy=h-190
		precioT=0
		for i in range(len(categorias)):
			libro.drawString(25,posy,categorias[i])
			libro.drawString(305,posy,str(pesos[i]))
			prec=self.obj_consulta.consultar_precio(categorias[i])
			libro.drawString(405,posy,str(prec[0][0]))
			precioT=precioT+round(prec[0][0]*pesos[i],2)
			libro.drawString(485,posy,str(round(prec[0][0]*pesos[i],2)))
			posy+=30

		xlist=[20,300,400,480,560]
		ylist=[h-105,h-135,h-165,h-195,h-225]
		libro.grid(xlist,ylist)
		libro.drawString(30,h-250,f'MONTO TOTAL ESTIMADO: {str(round(precioT,2))} SOLES')

		libro.drawImage("grafica.png", 0, h-550, width=550, height=250)	
		libro.save()		
		

		
		



	