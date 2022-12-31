from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('authentication', views.authentication, name="authentication"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name='logout'),
    path('privacy-policy', views.privacy, name='privacy-policy'),
    path('terms-and-conditions', views.terms, name='terms-and-conditions'),
    path('write-post', views.writePost, name='write-post'),
    path('transfer-point', views.transferPoint, name='transfer-point'),
    path('feedback', views.feedback, name='feedback'),
]