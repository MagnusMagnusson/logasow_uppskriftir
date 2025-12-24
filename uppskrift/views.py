from django.shortcuts import render
from .models import Uppskrift
from .models import Flokkur
from django.http import JsonResponse
from django.db.models import Q, CharField, TextField
from tinymce.models import HTMLField
import re

def get_grouped_uppskriftir(by_yfirflokkur = True):
    flokk_groups = []

    # fetch all yfirflokkar sorted by nafn and prefetch their related recipes
    yfirflokkar = Flokkur.objects.all()
    if by_yfirflokkur:
        yfirflokkar = yfirflokkar.filter(yfirflokkur=True)
    yfirflokkar.order_by('nafn').prefetch_related('uppskrift_set')

    for flokkur in yfirflokkar:
        uppskriftir_qs = flokkur.uppskrift_set.all().order_by('nafn')
        if uppskriftir_qs.exists():
            flokk_groups.append({'flokkur': flokkur, 'name': flokkur.nafn, 'uppskriftir': list(uppskriftir_qs)})

    # collect ids of already grouped recipes and build "Uncategorized" group for the rest
    categorized_ids = {u.id for g in flokk_groups for u in g['uppskriftir']}
    uncategorized_qs = Uppskrift.objects.exclude(id__in=categorized_ids).order_by('nafn')
    if uncategorized_qs.exists():
        flokk_groups.append({'flokkur': None, 'name': 'Óflokkað', 'uppskriftir': list(uncategorized_qs)})

    return flokk_groups

def get_grouped_by_letter_uppskriftir():
    flokk_groups = []
    from string import ascii_uppercase


    for letter in ascii_uppercase:
        uppskriftir_qs = Uppskrift.objects.filter(nafn__istartswith=letter).order_by('nafn')
        if uppskriftir_qs.exists():
            flokk_groups.append({'flokkur': letter, 'name': letter, 'uppskriftir': list(uppskriftir_qs)})

    return flokk_groups

def index(request):
    querystring_sort = request.GET.get('sort', 'bokstafur')
    if querystring_sort == 'yfirflokkur':
        flokk_groups = get_grouped_uppskriftir(True)
    elif querystring_sort == 'flokkur':
        flokk_groups = get_grouped_uppskriftir(False)
    else:
        flokk_groups = get_grouped_by_letter_uppskriftir()

    flokkar = Flokkur.objects.all().order_by('nafn')

    return render(request, './index.html', {'grouped_uppskriftir': flokk_groups, 'flokkar': flokkar, 'current_sort': querystring_sort})

def recipe_detail(request, slug):
    uppskrift = Uppskrift.objects.get(slug=slug)
    return render(request, './recipe.html', {'uppskrift': uppskrift})



def recipe_filter(request):
    search_query = request.GET.get('q', '').strip()
    flokkar = request.GET.getlist('flokkar')
    print(flokkar)

    filters = Q()
    if search_query:
        filters &= (Q(nafn__icontains=search_query) |
                    Q(innihaldsefni__icontains=search_query) |
                    Q(uppskrift__icontains=search_query) |
                    Q(athugasemdir__icontains=search_query))
    if flokkar:
        filters &= Q(flokkar__nafn__in=flokkar)

    print(filters)
    filtered_uppskriftir = Uppskrift.objects.filter(filters).distinct().order_by('nafn')

    results = []
    for uppskrift in filtered_uppskriftir:
        results.append({
            'nafn': uppskrift.nafn,
            'slug': uppskrift.slug,
            'id': uppskrift.id
        })

    return JsonResponse({'results': results})