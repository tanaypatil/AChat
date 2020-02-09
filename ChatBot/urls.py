from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('files', files, name="files"),
    path('delete_file', delete_file, name="delete_file"),
    path('rating', rating, name="rating"),
    path('logout', logout_user, name="logout"),
]
