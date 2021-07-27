from django.urls import path
from accounts.views import LoginView, RegistrationView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_url'),
    path('register/', RegistrationView.as_view(), name='registration_url'),
]
