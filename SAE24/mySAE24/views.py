from django.shortcuts import render
from . import models

def index(request):
	data = list(models.data.objects.all())
	return render(request, "index.html",{"data":data,})


