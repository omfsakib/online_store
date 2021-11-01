from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerPage,name="register"),
    path('shopregister/',views.shopOwnerRegisterPage,name="shopregister"),
    path('token/',views.token_send,name="token_send"),
    path('success/',views.success,name="success"),
    path('verify/<auth_token>',views.verify,name="verify"),
    path('error/',views.error_page,name='error'),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('user/dashboard/',views.userPage,name='user-page'),
    path('account/',views.viewAccount,name='account'),
    path('account/edit/',views.accountSettings,name='edit_account'),
    path('change-password/',views.change_password,name = 'change_password'),
    path('', views.home,name='home'),
    path('products/', views.products,name='products'),
    path('customer/<str:pk>/', views.customers,name='customer'),
    path('create_order/<str:pk>/',views.createorder,name='create_order'),
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),
    path('mail',views.mail_letter,name='mail'),
]