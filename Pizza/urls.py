from . import views
from django.urls import path


urlpatterns = [
    path('ajax/pizza-options/<int:id>/',views.loadpizzaoptions,name='loadpizzaoptions'),
    path('ajax/pizza-option-selection-based-on-id/<int:option_id>/',views.optionbasedonselection,name="optionbasedonselection"),
]