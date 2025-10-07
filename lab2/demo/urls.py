from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('login-vuln', views.login_vuln, name='login_vuln'),
    path('login-safe', views.login_safe, name='login_safe'),
    path('admin-area', views.admin_area, name='admin_area'),
    path('logout', views.logout_view, name='logout'),
    path('init', views.init_seed, name='init_seed'),
]



