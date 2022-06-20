from django.db import models

#____________________________________________________________
class test1(models.Model):
    OKAY = models.CharField(max_length=100)


    def __str__(self):
        chaine = f"{self.OKAY}"
        return chaine


#____________________________________________________________
class test2(models.Model):
    OUHO = models.BigIntegerField(null=True)

    def __str__(self):
        chaine = f"{self.OUHO}"
        return chaine
