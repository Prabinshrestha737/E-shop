
from django.urls import path
from . import views 

from .views import * 

urlpatterns = [
    # path('', views.index, name="index"),
    path('', Index.as_view(), name="index"),
    path('signup', SignUp.as_view(), name='signup'),
    path('loginpage', Login.as_view(), name="login"),
    path('logout', views.logout, name="logout"),
    path('cart', Cart.as_view(), name="cart"),
]