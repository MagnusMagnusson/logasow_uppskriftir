from django.contrib import admin
from uppskrift.models import Uppskrift


# Dynamically create TabularInlines for any ManyToMany through models so relationships can be edited inline
m2m_inlines = []
for field in Uppskrift._meta.get_fields():
    if getattr(field, "many_to_many", False) and getattr(field, "remote_field", None):
        through = field.remote_field.through
        # skip if no through model available
        if through is None:
            continue
        inline_name = f"{Uppskrift.__name__}{field.name.capitalize()}Inline"
        Inline = type(inline_name, (admin.TabularInline,), {"model": through, "extra": 1})
        m2m_inlines.append(Inline)

class UppskriftAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = "Uppskriftir"
    # make all model fields editable except the primary key 'id'
    exclude = ("id",)
    # allow searching and ordering by name
    search_fields = ("nafn",)
    ordering = ("nafn",)
    list_display = ("nafn",)
    # allow inline editing/adding of many-to-many relationships
    inlines = m2m_inlines
    

admin.site.register(Uppskrift, UppskriftAdmin)