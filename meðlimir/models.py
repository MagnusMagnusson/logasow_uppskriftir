from django.db import models

class Meðlimur(models.Model):
    class Meta:
        verbose_name_plural = "Meðlimir"
    id = models.AutoField(primary_key=True)
    nafn = models.CharField(max_length=64, null=False)

    def __str__(self):
        return self.nafn

class skodun(models.Model):
    class skodunarflokkur(models.TextChoices):
            HATAR = '0', ('Hatar')
            MISLIKAR = '1', ('Mislíkar')
            HLUTLAUS = '2', ('Hlutlaus')
            LIKAR = '3', ('Líkar')
            ELSKAR = '4', ('Elskar')

    id = models.AutoField(primary_key=True)
    medlimur = models.ForeignKey(Meðlimur, on_delete=models.CASCADE)
    uppskrift = models.ForeignKey('uppskrift.Uppskrift', on_delete=models.CASCADE)
    skodun = models.CharField(max_length=1, choices=skodunarflokkur.choices, null=False)
    athugasemd = models.TextField()