from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('capteurs/',views.index_capteurs),
    path('capteurs/<int:id>/',views.mesures_capteurs),
    path('delete/capteurs/<int:id>/',views.delete_capteur),
    path('update/capteurs/<int:id>/',views.update)
]