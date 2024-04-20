import imp
from operator import imod
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('issue_certificate/',views.issue_certificate,name="issue_certificate"),
    path('verify_certificate/',views.verify_certificate,name="verify_certificate"),
    path('apply_masters/',views.apply_masters,name="apply_masters"),
    path('view_certificates/',views.view_certificates,name="view_certificates"),

]