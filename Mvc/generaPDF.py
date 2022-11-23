from reportlab.pdfgen import canvas as can
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image


class Reporte(object):
	def __init__(self):		
		pdfmetrics.registerFont(TTFont('Vera','Vera.ttf'))		
	def Reporte_(self,canvas):
		libro=can.Canvas('Reporte.pdf',pagesize=A4)
		w,h=landscape(A4)		
		libro.drawString(20,h-20,f'REPORTE GENERAL')
		libro.drawString(20,h-35,f'USUARIO: ')
		libro.drawString(20,h-50,f'DESDE: ')
		libro.drawString(20,h-50,f'HASTA: ')	
		libro.save()

		canvas.update()
		canvas.postscript(file="file_name.ps", colormode='color') 



	