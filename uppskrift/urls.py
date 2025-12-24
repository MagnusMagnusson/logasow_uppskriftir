from uppskrift.views import index, recipe_detail, recipe_filter
from django.urls import path   

urlpatterns = [
    path('', index, name='index'),
    path('<slug:slug>/', recipe_detail, name='recipe_detail'),
    path('api/filter/', recipe_filter, name='recipe_filter')
]

