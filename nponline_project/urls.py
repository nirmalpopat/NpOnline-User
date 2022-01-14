from django.contrib import admin
from django.urls import path
from sells import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.AddSell.as_view(), name='AddSell'),
    path('stocklist/', views.StockListView.as_view(), name='liststock'),
    path('viewlist/', views.ReportView.as_view(), name='viewlist'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]
