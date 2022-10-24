from django.urls import path

from . import views
urlpatterns=[
    path('register/', views.UserRegistration.as_view(), name="register"),
    path('login/',views.UserLogin.as_view(),name="login"),
    path('verify_token/<str:token>/',views.VerifyToken.as_view(),name="verify_token"),
    # # path('user_reg/',views.user_reg,name="user_reg"),
    # # path('user_login/',views.user_login,name="user")
    # path('index/',views.Index.as_view(),name="index")


]