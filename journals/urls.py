from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("add_entry/", views.add_entry, name="add_entry"),
    path("delete_all_entries/", views.delete_all_entries, name="delete_all_entries"),
    path("delete_entry/<int:entry_id>", views.delete_entry, name="delete_entry")
]