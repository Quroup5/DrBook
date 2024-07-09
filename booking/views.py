from django.shortcuts import render

# Create your views here.
from django.urls import path
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Transaction

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'


class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'transaction'


class TransactionCreateView(CreateView):
    model = Transaction
    template_name = 'transactions/transaction_form.html'
    fields = ['patient', 'price']
    success_url = reverse_lazy('transaction_list')