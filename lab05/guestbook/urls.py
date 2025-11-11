"""
URL configuration for guestbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path

from guests import views as guest_views
from portals import views as portal_views

urlpatterns = [
    path('admin/panel/', portal_views.AdminPanelView.as_view(), name='admin-panel'),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('', guest_views.list_safe, name='safe'),
    path('vulnerable/', guest_views.list_vulnerable, name='vulnerable'),
    path('manager/workspace/', portal_views.ManagerWorkspaceView.as_view(), name='manager-workspace'),
    path('manager/accounts/', portal_views.AccountListView.as_view(), name='manager-accounts'),
    path('manager/accounts/create/', portal_views.AccountCreateView.as_view(), name='manager-account-create'),
    path('manager/accounts/<int:pk>/edit/', portal_views.AccountUpdateView.as_view(), name='manager-account-edit'),
    path('manager/accounts/<int:pk>/delete/', portal_views.AccountDeleteView.as_view(), name='manager-account-delete'),
]
