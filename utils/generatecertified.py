
import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from members.models import Member
from .forms import *
from .models import Event, Spectator
from django.utils import formats
import json
from django.core.mail import send_mail
from datetime import timezone
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO

def generateCertificates(request):

event = Event.objects.filter(request.slug==slug)
spectators = Spectator.objects.filter(confirmed=True)

mes_ext = {1: 'Janeiro', 2 : 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio',6:'Junho',7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',11:'Novembro',12:'Dezembro'}

data=time.strftime("%d")
data+=" de "
data+=mes_ext[int(time.strftime("%m"))]
data+=" de "
data+=time.strftime("%Y")

response = HttpResponse(content_type='application/pdf')
response['Content-Disposition'] = 'attachment; filename="Certificados.pdf"'

buffer = BytesIO()
pdf =  canvas.Canvas(buffer, (width,height));

for spec in spectators:
  pdf.drawImage('./images/Certificado.jpg',0,0,width,height)
  pdf.setFont('Helvetica',80, leading=None)
  pdf.drawCentredString(1750,1450,"Certicamos que ")
  pdf.setFont('Helvetica-Bold',80, leading=None)
  pdf.drawCentredString(1750,1350, spec.name)
  pdf.setFont('Helvetica',80, leading=None)
  pdf.drawCentredString(1750,1250,"participou do "+event.name)
  pdf.drawCentredString(1750,1150,"no "+event.address)

  if event.start_date != event.end_date:
    if (event.end_date.days - event_start_date.days) < 3:
      pdf.drawCentredString(1750,1050,"em "+event.start_date.day+" e "+ event.end_date.day +" de "+ mes_ext[event.start_date.month]+" de "+even.start_date.year+ " das "+event.beginTime+" às "+event.endTime)
    else:
      if event.end_date.year != event_start_date.year:
        pdf.drawCentredString(1750,1050,"em "+event.start_date.day+" de "+ mes_ext[event.start_date.month]+" de "+even.start_date.year+" a " + event.end_date.day+" de "+ mes_ext[event.end_date.month]+" de "+even.end_date.year+" das "+event.beginTime+" às "+event.endTime)
      else:
        pdf.drawCentredString(1750,1050,"em "+event.start_date.day+" a "+ event.end_date.day +" de "+ mes_ext[event.start_date.month]+" de "+even.start_date.year+ " das "+event.beginTime+" às "+event.endTime)
  else:
    pdf.drawCentredString(1750,1050,"em "+event.start_date.day+" de "+ mes_ext[event.start_date.month]+" de "+even.start_date.year+ " das "+event.beginTime+" às "+event.endTime)

  pdf.drawCentredString(840,700,"Belo Horizonte, "+ data)
  pdf.showPage()

pdf.save()
p = buffer.getvalue()
buffer.close()
response.write(p)

return response
