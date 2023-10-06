from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.get_login, name='login'),
    path('valid_login/', views.valid_login, name='valid_login'),
    path('logout/', views.set_logout, name='logout'),
    path('register/', views.register_client, name='register'),
    path('valid_register/', views.valid_register, name='valid_register'),
    path('profile/', views.get_profile, name='profile'),
    path('upload-photo/', views.upload_photo_user, name='upload_photo'),
    path('profile-update/', views.update_name_email, name='update_datas'),
    path('change-password/', views.change_password, name='change_password'),
]
