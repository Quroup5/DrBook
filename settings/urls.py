from django.urls import path
from .views import (
    TransactionListView,
    TransactionDetailView,
    TransactionCreateView,
)
app_name = "settings"
urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
    path('transactions/new/', TransactionCreateView.as_view(), name='transaction_create'),
]