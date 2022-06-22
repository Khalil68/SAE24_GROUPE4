from django.shortcuts import render, HttpResponseRedirect
from . import models
from .forms import capteurForm

# Create your views here.

def index(request):
    data = list(models.data.objects.all())
    count = len(data)
    for i in data:
        capteur = models.capteur.objects.get(id=i.capteur)
        i.piece = capteur.piece
        i.emplacement = capteur.emplacement
        i.capteur_nom = capteur.nom
    data.reverse()
    return render(request, 'index.html',{'data':data,'count':count})

def update(request,id):
    if request.method == "POST":
        form = capteurForm(request.POST)
        if form.is_valid():
            capteur = form.save(commit=False)
            capteur.id = id
            capteur.piece = models.capteur.objects.get(pk=id).piece
            capteur.save()
            return HttpResponseRedirect("/capteurs")
    else:
        capteur = models.capteur.objects.get(pk=id)
        form = capteurForm(capteur.dico())
        return render(request,"update.html",{"form":form, "id":id, "capteur": capteur})


def index_capteurs(request):
    data = list(models.capteur.objects.all())
    count = len(data)
    return render(request, 'index_capteurs.html', {'liste': data, 'count': count})

def mesures_capteurs(request,id):
    data = list(models.data.objects.filter(capteur=id))
    count = len(data)
    for i in data:
        capteur = models.capteur.objects.get(id=i.capteur)
        i.piece = capteur.piece
        i.emplacement = capteur.emplacement
        i.capteur_nom = capteur.nom
    data.reverse()
    return render(request, 'index.html', {'data': data, 'count': count})

def delete_capteur(request,id):
    capteur = models.capteur.objects.get(pk=id)
    data = list(models.data.objects.filter(capteur=id))
    for i in data:
        i.delete()
    capteur.delete()
    return HttpResponseRedirect('/capteurs')