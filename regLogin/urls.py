from django.urls import path
from . import views

urlpatterns = [

    path('',views.HomePage,name = 'HomePage'),
    path('newUserRegister/',views.UserRegistration,name = "newUserRegister"),
    path('UserLogin/',views.Login,name = "UserLogin"),
    path('Logout/',views.Logout,name = "Logout"),
    path('password-reset/',views.PasswordResetView,name = "password_reset"),
    path('password-reset/done/',views.PasswordResetDoneView,name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',views.PasswordResetConfirmView,name='password_reset_confirm'),
    path('password-reset-complete/',views.PasswordResetCompleteView,name='password_reset_complete'),
    path('signed-In/',views.Profile,name = "signedIn")
]
