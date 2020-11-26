from django.urls import path, include

from .views import page_detail_view


urlpatterns = [
    path('p/<slug:slug>/', page_detail_view, name='page-detail'),
]