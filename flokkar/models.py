from django.db import models

class Flokkur(models.Model):
    class Meta:
        verbose_name_plural = "Flokkar"
    nafn = models.CharField(max_length=64, null=False, primary_key=True)
    yfirflokkur = models.BooleanField(default=False)

    def __str__(self):
        return self.nafn