from django.urls import path, reverse_lazy
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('entry/create/', views.EntryCreateView.as_view(), name='entry-create'),
    path('entry/<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry-delete'),
    path('entry/<int:pk>/update/', views.EntryUpdateView.as_view(), name='entry-update'),
    path('box/', views.BoxView.as_view(), name = 'box'),
]

