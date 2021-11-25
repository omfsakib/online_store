from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

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
    path('flash_sell/', views.flashSell,name='flash'),
    path('products/setting/<str:pk>/', views.productSetting, name='product_setting'),
    path('customer/<str:pk>/', views.customers,name='customer'),
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    path('update_stock/<str:pk>/',views.updateStock,name='update_stock'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),
    path('mail/',views.mail_letter,name='mail'),
    path('create/tag/',views.createTag,name='tag'),
    path('create/category/',views.createCategory,name='category'),
    path('reset-password/', PasswordResetView.as_view(
        template_name= 'accounts/reset_password.html',
        success_url=reverse_lazy('password_reset_done'),
        email_template_name= 'accounts/reset_password_email.html'
    ), name='reset_password'),

    path('reset-password/done/',PasswordResetDoneView.as_view(
        template_name= 'accounts/reset_password_done.html'
    ),name= 'password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(
        template_name= 'accounts/reset_password_confirm.html',
         success_url=reverse_lazy('password_reset_complete'),
    ),name= 'password_reset_confirm' ),
    path('reset-password/complete/',PasswordResetCompleteView.as_view(
        template_name= 'accounts/reset_password_complete.html'
    ),name ='password_reset_complete')
]