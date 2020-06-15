from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'),
         name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'),
         name='about'),
    path('admin/', admin.site.urls),
]
