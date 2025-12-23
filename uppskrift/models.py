from django.db import models
from flokkar.models import Flokkur
from meðlimir.models import Medlimur, skodun
from tinymce.models import HTMLField

class Uppskrift(models.Model):
    class Meta:
        verbose_name_plural = "Uppskriftir"
    id = models.AutoField(primary_key=True)
    nafn = models.CharField(max_length=64, null = False)
    slug = models.SlugField(max_length=64, null=False, unique=True)
    innihaldsefni = HTMLField(blank=True)
    uppskrift = HTMLField(blank=True)
    uppruni = models.CharField(max_length=128, blank=True)
    athugasemdir = models.TextField(blank=True)
    flokkar = models.ManyToManyField(to=Flokkur, blank=True)
    skodanir = models.ManyToManyField(to=Medlimur, through=skodun, related_name='medlimaskodanir', blank=True)

    def __str__(self):
        return self.nafn