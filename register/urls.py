from django.urls import path
from . import views

urlpatterns = [
    path('', views.logo_page, name='logo'),
    path('register/', views.register, name='register'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('owner/login/', views.owner_login, name='owner_login'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('logout/', views.owner_logout, name='owner_logout'),
    path('player-decision/<int:player_id>/', views.player_decision, name='player_decision'),
    path('media/<path:file_path>', views.serve_media_file, name='serve_media_file'),
]
