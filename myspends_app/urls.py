from django.urls import path

from . import views

urlpatterns = [
    path('payments_list/', views.payments_list, name='payments_list'),
    path('payment_details/<int:payment_id>/', views.payment_details, name='payment_details'),
    path('new_payment/', views.new_payment, name='new_payment'),
    path('delete_payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('edit_payment/<int:payment_id>/', views.edit_payment, name='edit_payment'),
]
