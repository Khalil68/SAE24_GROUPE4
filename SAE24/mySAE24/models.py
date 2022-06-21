from django.db import models

#____________________________________________________________
class capteur1(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nom_capteur = models.CharField(max_length=100)
    piece = models.CharField(max_length=100)
    emplacement_capteur = models.CharField(max_length=100)


    def __str__(self):
        chaine = f"{self.id}"
        return chaine

    #def dictionnaire(self):
     #   return {"nom": self.nom, "descriptif": self.descriptif}
#____________________________________________________________
class capteur2(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nom_capteur = models.CharField(max_length=100)
    piece = models.CharField(max_length=100)
    emplacement_capteur = models.CharField(max_length=100)


    def __str__(self):
        chaine = f"{self.id}"
        return chaine

    #def dictionnaire(self):
     #   return {"nom": self.nom, "descriptif": self.descriptif}