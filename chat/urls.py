from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.homePage),
    path('me/', views.MemberApiView.as_view()),
    path('lookup/', views.lookUp),
    path('chat/<int:id>/', views.Chat1on1)
]