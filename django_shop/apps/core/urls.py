from django.urls import path, include

from apps.core.views import (
    homepage_view,
    RobotsTxtView,
    SitemapXmlView,
)


urlpatterns = [
    path('', homepage_view, name='homepage'),

    path('robots.txt', RobotsTxtView.as_view()),
    path('sitemap.xml', SitemapXmlView.as_view()),
]