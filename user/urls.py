from django.conf.urls import url
from .views import *
from django.urls import path

urlpatterns = [

    path('register/', ApiRegistration.as_view(), name='register'),
    path('login/', ApiLogin.as_view(), name="login"),
    # path('',template,name="landing_page"),
    # path('dashboard',dashboard,name="dashboard"),
    # path("testing",testing,name="testing"),
    path("activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",activate, name='activate'),
    # path("user_logout/$", logout_view,name="user_logout")

]
