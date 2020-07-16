from django.shortcuts import render
from django.http import Http404

from .models import Pages


def page_detail_view(request, slug):
    try:
        page = Pages.objects.filter(active=True).get(slug=slug)
    except:
        raise Http404

    context = {
        'page_title': page.title,
        'page': page
    }
    return render(request, 'pages/page_detail.html', context=context)
