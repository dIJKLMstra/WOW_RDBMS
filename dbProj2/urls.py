"""dbProj2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from wowModel import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('index', views.index),
    path('register', views.register),
    path('cust_details/<int:id>', views.cust_details),
    path('accounts/login/', views.login),
    path('reset_password', views.reset_password),
    path('info', views.profile),
    path('edit_profile', views.edit_profile),
    path('logout', views.logout),
    path('admin/', admin.site.urls),
    path('emp', views.record_add),
    path('show', views.record_show),
    path('edit/<int:id>', views.record_update),
    path('update/<int:id>', views.record_update),
    path('delete/<int:id>', views.record_destroy),
    path('vehi', views.vehicle_add),
    path('vehi_show', views.vehicle_show),
    path('vehi_update/<int:id>', views.vehicle_update),
    path('vehi_delete/<int:id>', views.vehicle_destroy),
    path('coupon', views.indi_cust_coupon),
    path('invoice/<int:id>', views.gene_invoice),
    path('payment/<int:id>', views.payment)
]
