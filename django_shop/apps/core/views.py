from django.shortcuts import render

# from djanago.views.generic import ListView, DetailView, TemplateView
from django.views.generic import TemplateView

from apps.shop.models import Products, Categories
from apps.pages.models import Pages


def homepage_view(request):
    context = {
        'page_title': 'Casekam – магазин чехлов для телефонов',
        'page_description': '',
        'products': Products.objects.filter(active=True).order_by('?')[:6],
        'categories': Categories.objects.all().order_by('name'),
    }
    return render(request, 'homepage.html', context=context)


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'


class SitemapXmlView(TemplateView):
    template_name = 'sitemapxml.html'
    content_type = 'application/xml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Products.objects.filter(active=True).order_by('-updated')
        context['categories'] = Categories.objects.all()
        context['pages'] = Pages.objects.filter(active=True)
        return context


def error_404(request, exception):
    context = {
        'page_title': '404',
        'page_description': 'Страница не найдена =((',
    }
    return render(request, 'errors/404.html', context=context)