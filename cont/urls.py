from django.contrib import admin
from django.urls import path ,include
from .views import HomePage,Login,singup,logout_view,SupplierPage,customer_page,Manger_page,actual_date

urlpatterns = [

    path('', HomePage , name='Home'),
    path('Login', Login , name='login'),
    path('singup', singup , name='singup'),
    path('logout_view', logout_view , name='logout_view'),
    path('SupplierPage', SupplierPage , name='SupplierPage'),
    path('customer_page', customer_page , name='customer_page'),
    path('Manger_page', Manger_page , name='Manger_page'),
    path('actual_date', actual_date , name='actual_date'),



    

]