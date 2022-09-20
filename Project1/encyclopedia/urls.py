from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry_view, name="entry_view"),
    path("wiki/<str:entry>", views.entry_view, name="entry_view"),
    path("new/", views.new_entry, name="new_entry")
]
