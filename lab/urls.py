from django.urls import path

from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    path('lablogin', LoginView.as_view(template_name='lab/lablogin.html'),name='lablogin'),
    path('labsignup', views.lab_signup_view,name='labsignup'),
    path('lab-dashboard', views.lab_dashboard_view,name='lab-dashboard'),
    path('make-request', views.make_request_view,name='make-request'),
    path('my-request', views.my_request_view,name='my-request'),
]