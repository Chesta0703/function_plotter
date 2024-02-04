from django.urls import path

from . import views

urlpatterns = [
    # Commented out the index view path
    # path("", views.index, name="index"),
    path("networked-epi/", views.networked_epi_view, name="networked_epi"),
    # Add other paths here as needed
]

