"""App URLs"""

from django.urls import path, re_path

from assets import views
from assets.api import api

app_name: str = "assets"

urlpatterns = [
    path("", views.index, name="index"),
    path("add_corp/", views.add_corp, name="add_corp"),
    path("add_char/", views.add_char, name="add_char"),
    path("buy", views.create_order, name="create_order"),
    # -- API System
    re_path(r"^api/", api.urls),
]
