from uppskrift.views import index, recipe_detail
from django.urls import path   

urlpatterns = [
    path('', index, name='index'),
    path('<slug:slug>/', recipe_detail, name='recipe_detail')
]

