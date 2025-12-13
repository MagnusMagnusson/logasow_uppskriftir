from django.contrib import admin
from flokkar.models import Flokkur

class FlokkurAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = "Flokkar"
        verbose_name = "Flokkar"

admin.site.register(Flokkur, FlokkurAdmin)