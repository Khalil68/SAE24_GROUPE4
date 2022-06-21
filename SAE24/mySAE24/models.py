from django.db import models

class capteur(models.Model):
    nom = models.CharField(max_length=100)
    piece = models.CharField(max_length=100)
    emplacement = models.CharField(max_length=100)

    def __str__(self):
        chaine = f"{self.nom}"
        return chaine

    def dico(self):
        return {"nom": self.nom,"piece": self.piece, "emplacement": self.emplacement}


class data(models.Model):
    data = models.CharField(max_length=200)
    timestamp = models.CharField(max_length=200)
    capteur = models.ForeignKey("capteur", on_delete=models.CASCADE,blank=False)

    def __str__(self):
        chaine = self.data + "," + self.timestamp + "," + capteur.objects.get(id=self.capteur).piece + " | " + capteur.objects.get(id=self.capteur).nom
        return chaine

    def dico(self):
        return {"nom": self.data,"piece": self.timestamp, "emplacement": self.capteur}