from django.urls import path
from library import views

urlpatterns = [
    path('list/', views.CartListAPIView.as_view()),
    path('add-item/', views.CartAddItemAPIView.as_view()),
    path('remove-item/', views.CartRemoveItemAPIView.as_view()),
    path('create-order/', views.CreateOrderAPIView.as_view()),
    
]