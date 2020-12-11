"""grizo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from masterpiece import  views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('masterpiece.urls')),

    path('normal_res/', views.normal_res, name='normal_res'),

    path('get_res/<str:get_message1>/<str:get_message2>', views.get_res, name='get_res'),
    path('get_res/', views.get_res, name='get_res'),
    path('post_res/', views.post_res, name='post_res'),

    path('select_res/', views.select_res, name='select_res'),
    path('delete_res/', views.delete_res, name='delete_res')
]