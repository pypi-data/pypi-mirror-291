"""Routes."""

from django.urls import path

from . import views

app_name = "metenox"

urlpatterns = [
    path("", views.index, name="index"),
    path("add_owner", views.add_owner, name="add_owner"),
    path("corporations", views.corporations, name="corporations"),
    path("moons_data", views.MoonListJson.as_view(), name="moons_data"),
    path("moons_fdd_data", views.moons_fdd_data, name="moons_fdd_data"),
    path("prices", views.prices, name="prices"),
]
