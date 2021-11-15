from django.urls import path
from . import views


urlpatterns = [
    path('store/',views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('shops/',views.shops,name="shops"),
    path('view_shop/<str:pk>/',views.view_shops,name="view_shop"),
    path('view/<str:pk>/',views.productView,name="view"),
    path('delete_review/<str:pk>/',views.deleteReview,name="delete_review"),
    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),
]