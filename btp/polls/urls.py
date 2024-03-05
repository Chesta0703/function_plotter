from django.urls import path

from . import views

urlpatterns = [
    # Commented out the index view path
    # path("", views.index, name="index"),
    path("networked-epi/", views.networked_epi_view, name="networked_epi"),
    path('get_sir_plot/<int:node_id>/', views.get_sir_plot, name='get_sir_plot'),
    # Add other paths here as needed
]


