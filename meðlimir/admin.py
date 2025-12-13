from django.contrib import admin
from uppskrift.models import Uppskrift
from meðlimir.models import Meðlimur

from meðlimir.models import Meðlimur

# Dynamically build TabularInlines for any ManyToMany on Uppskrift that points to Meðlimur.
def _make_through_inline(through, name):
    class UppskriftThroughInline(admin.TabularInline):
        model = through
        extra = 0
        verbose_name = name
        verbose_name_plural = name
    return UppskriftThroughInline

_inlines = []
for f in Uppskrift._meta.get_fields():
    # consider only many-to-many fields that have a remote_field and a through model
    if getattr(f, "many_to_many", False) and getattr(f, "remote_field", None):
        remote = getattr(f.remote_field, "model", None)
        # remote may be the class object; check identity with Meðlimur
        if remote is Meðlimur:
            through_model = f.remote_field.through
            _inlines.append(_make_through_inline(through_model, f.name))

class MeðlimurAdmin(admin.ModelAdmin):
    # show basic representation and attach any Uppskrift inlines found
    class Meta:
        verbose_name_plural = "Meðlimir"
    list_display = ("__str__",)
    inlines = _inlines
    search_fields = ("__str__",)

admin.site.register(Meðlimur, MeðlimurAdmin)
