from django.urls import path
from accounts.views import LoginView, RegistrationView, logout_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_url'),
    path('register/', RegistrationView.as_view(), name='registration_url'),
    path('logout/', logout_view, name='logout_url'),
]
