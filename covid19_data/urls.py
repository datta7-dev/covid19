from django.urls import path
from covid19_data import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
]
