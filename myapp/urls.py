from django.urls import path,include
from . import views
from django.contrib import admin



urlpatterns=[
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name="register"),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('gallery/',views.gallery,name='gallery'),
    path('services/',views.services,name='services'),
    path('promo/',views.promo,name='promo'),
    path('testimonials/',views.testimonials,name='testimonials'),
    
    path('booking/',views.booking,name='booking'),
    path('servicestatus/',views.servicestatus,name='servicestatus'),
    path('payment/',views.payment,name='payment'),
    
]
