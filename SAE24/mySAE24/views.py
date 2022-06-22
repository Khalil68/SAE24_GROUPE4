from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from . import models
from .forms import capteurForm
from django.http import FileResponse
from fpdf import FPDF


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
    return render(request, 'index.html', {'data': data, 'count': count})


def update(request, id):
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
        return render(request, "update.html", {"form": form, "id": id, "capteur": capteur})


def index_capteurs(request):
    data = list(models.capteur.objects.all())
    count = len(data)
    return render(request, 'index_capteurs.html', {'liste': data, 'count': count})


def mesures_capteurs(request, id):
    data = list(models.data.objects.filter(capteur=id))
    count = len(data)
    for i in data:
        capteur = models.capteur.objects.get(id=i.capteur)
        i.piece = capteur.piece
        i.emplacement = capteur.emplacement
        i.capteur_nom = capteur.nom
    data.reverse()
    return render(request, 'index.html', {'data': data, 'count': count})


def delete_capteur(request, id):
    capteur = models.capteur.objects.get(pk=id)
    data = list(models.data.objects.filter(capteur=id))
    for i in data:
        i.delete()
    capteur.delete()
    return HttpResponseRedirect('/capteurs')


def sae24_pdf(request ,id):
    data = models.data.objects.get(pk=id)
    capteur = models.capteur.objects.get(pk=id)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=16)
    pdf.cell(200, 10, txt="Voici les éléments de notre capteur :", ln=2, align='C')
    pdf.cell(200, 10, txt="La température est de  " + str(data.data), ln=2, align='C')
    pdf.cell(200, 10, txt="Il a était mis a jour à  " + str(data.timestamp), ln=2, align='C')
    pdf.cell(200, 10, txt="Son emplacement est à " + str(capteur.emplacement), ln=2, align='C')
    pdf.cell(200, 10, txt="Il se trouve dans " + str(capteur.piece), ln=2, align='C')
    pdf.cell(200, 10, txt="L'ID du capteur est " + str(capteur.nom), ln=2, align='C')
    pdf.output('SAE24.pdf')
    response = FileResponse(open("SAE24.pdf"))
    return response
