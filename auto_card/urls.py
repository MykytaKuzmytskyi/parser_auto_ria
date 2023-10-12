from django.urls import path

from auto_card.views import start_pars

app_name = "auto_card"

urlpatterns = [
    path("start_pars/", start_pars),
]
