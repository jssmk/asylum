# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView
from creditor.models import Transaction, TransactionTag
from django.db.models import Sum
from django.utils import timezone


class TransactionMonthView(ListView, year, month):
   model = Transaction
   template_name = "admin/table.html"
#   def get(self, request, *args, **kwargs):
#      print(request.GET.get('y', ''))
#      print(request.GET.get('m', ''))
#      return super(TransactionTableView, self).get(request, *args,**kwargs)
   
   param_year = timezone.now().year
   param_month = timezone.now().month
   param_tag = 0
   def get_queryset(self):
      self.param_year = self.request.GET.get('y', timezone.now().year)
      self.param_month = self.request.GET.get('m', timezone.now().month)
      self.param_tag = int(self.request.GET.get('tag', 0))
      print(self.param_year)
      print(self.param_month)
      print(TransactionTag.objects.values_list('pk', flat=True))
      print(self.param_tag) # vain jos on jokin sellainen numero joka on käytössä
      if(self.param_tag in TransactionTag.objects.values_list('pk', flat=True)):
         print("tag!")
         return Transaction.objects.filter(stamp__year=self.param_year).filter(stamp__month=self.param_month).filter(tag__pk=self.param_tag)
      return Transaction.objects.filter(stamp__year=self.param_year).filter(stamp__month=self.param_month)

   def get_context_data(self, **kwargs):
      context = super(TransactionTableView, self).get_context_data(**kwargs)
      context['income'] = self.get_queryset().filter(amount__gte=0).aggregate(sum=Sum('amount'))
      context['receivables'] = self.get_queryset().filter(amount__lt=0).aggregate(sum=Sum('amount'))
      context['total'] = self.get_queryset().aggregate(sum=Sum('amount'))
      context['year'] = self.param_year
      context['month'] = self.param_month
      
      return context


class TransactionYearView(ListView):
   model = Transaction
   template_name = "admin/table.html"
#   def get(self, request, *args, **kwargs):
#      print(request.GET.get('y', ''))
#      print(request.GET.get('m', ''))
#      return super(TransactionTableView, self).get(request, *args,**kwargs)
   
   param_year = timezone.now().year
   param_tag = 0
   def get_queryset(self):
      self.param_year = self.request.GET.get('y', timezone.now().year)
      self.param_tag = int(self.request.GET.get('tag', 0))
      print(self.param_year)
      print(TransactionTag.objects.values_list('pk', flat=True))
      print(self.param_tag) # vain jos on jokin sellainen numero joka on käytössä
      if(self.param_tag in TransactionTag.objects.values_list('pk', flat=True)):
         print("tag!")
         return Transaction.objects.filter(stamp__year=self.param_year).filter(tag__pk=self.param_tag)
      return Transaction.objects.filter(stamp__year=self.param_year)

   def get_context_data(self, **kwargs):
      context = super(TransactionTableView, self).get_context_data(**kwargs)
      context['income'] = self.get_queryset().filter(amount__gte=0).aggregate(sum=Sum('amount'))
      context['receivables'] = self.get_queryset().filter(amount__lt=0).aggregate(sum=Sum('amount'))
      context['total'] = self.get_queryset().aggregate(sum=Sum('amount'))
      context['year'] = self.param_year
      
      return context