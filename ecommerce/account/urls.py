from django.urls import path

from . import views

urlpatterns= [

    path('register',views.register,name='register'),

    #Email verification urls

    path('email-verification/<str:uidb64><str:token>/', views.email_verification, name='email-verification'),

    path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),

    
    path('email-verification-success', views.email_verification_success, name='email-verification-success'),


    path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),

    #Login/Logout urls

    path('my-login',views.my_login,name='my-login'),

    path('dashboard',views.dashboard,name='dashboard'),

    path('user-logout',views.user_logout,name='user-logout'),

    #shipping

    path('manage-shipping',views.manage_shipping,name='manage-shipping'),



]