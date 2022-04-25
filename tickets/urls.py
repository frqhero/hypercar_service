from django.urls import path, include
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path('menu', views.ShowMenu),
    path('menu/', RedirectView.as_view(url='/menu')),
    path('welcome', views.WelcomeView.as_view()),
    path('welcome/', RedirectView.as_view(url='/welcome')),
    path('get_ticket/inflate_tires', views.InflateTires),
    path('get_ticket/inflate_tires/',
         RedirectView.as_view(url='/get_ticket/inflate_tires')),
    path('get_ticket/change_oil', views.ChangeOil),
    path('get_ticket/change_oil/',
         RedirectView.as_view(url='/get_ticket/change_oil')),
    path('get_ticket/diagnostic', views.Diagnostic),
    path('get_ticket/diagnostic/',
         RedirectView.as_view(url='/get_ticket/diagnostic')),
    path('processing', views.OperatorInterface),
    path('processing/', RedirectView.as_view(url="/processing")),
    path('next', views.process_next),
    path('next/', RedirectView.as_view(url='/next'))
]
