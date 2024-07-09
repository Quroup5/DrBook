from django.urls import path
from .views import (
    TransactionListView,
    TransactionDetailView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,
)
app_name = "settings"
urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
    path('transactions/new/', TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
]