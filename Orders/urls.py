from . import views
from django.urls import path


urlpatterns = [
    path('creatingorder/',views.create_order,name="create_order"),
    path('showorder/<int:id>/',views.view_order,name="view_order"),   
]