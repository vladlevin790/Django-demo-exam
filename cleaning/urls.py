from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='order_lists'), name='logout'),
    path('',views.index, name='order_lists'),
    path('create_order/', views.create_order, name="create_order"),
]
