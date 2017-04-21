# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView
from creditor.models import Transaction, TransactionTag
from django.db.models import Sum
from django.utils import timezone
from django.db.models import Count

class TransactionMonthView(ListView):
   model = Transaction
   template_name = "admin/table.html"
   
   #param_year = timezone.now().year
   #param_month = timezone.now().month
   param_tag = 0
   def get_queryset(self):
      
      self.param_year = self.kwargs['year']
      self.param_month = self.kwargs['month']
      if('tag' in self.kwargs):
        self.param_tag = int(self.kwargs['tag'])
      
      if(self.param_tag in TransactionTag.objects.values_list('pk', flat=True)):
         return Transaction.objects.filter(stamp__year=self.param_year).filter(stamp__month=self.param_month).filter(tag__pk=self.param_tag)
      
      return Transaction.objects.filter(stamp__year=self.param_year).filter(stamp__month=self.param_month)
   
   
   def get_context_data(self, **kwargs):
      context = super(TransactionMonthView, self).get_context_data(**kwargs)
      context['income'] = self.get_queryset().filter(amount__gte=0).aggregate(sum=Sum('amount'))
      context['receivables'] = self.get_queryset().filter(amount__lt=0).aggregate(sum=Sum('amount'))
      context['total'] = self.get_queryset().aggregate(sum=Sum('amount'))
      context['year'] = self.param_year
      context['month'] = self.param_month.rjust(2, "0")
      context['months'] = ['01','02','03','04','05','06','07','08','09','10','11','12']
      context['years'] = [d.year for d in Transaction.objects.datetimes('stamp', 'year')]
      return context

class TransactionYearView(ListView):
   model = Transaction
   template_name = "admin/table_year.html"
   
   param_year = timezone.now().year
   param_tag = 0
   def get_queryset(self):
      
      if('year' in self.kwargs):
         self.param_year = self.kwargs['year']
      if('tag' in self.kwargs):
         self.param_tag = int(self.kwargs['tag'])
      
      #if(self.param_tag in TransactionTag.objects.values_list('pk', flat=True)):
         #return Transaction.objects.filter(stamp__year=self.param_year).filter(tag__pk=self.param_tag)
      
      return Transaction.objects.filter(stamp__year=self.param_year)#.annotate(sum_income=Sum('amount'))
   
   
   def get_context_data(self, **kwargs):
      context = super(TransactionYearView, self).get_context_data(**kwargs)
      context['receivables'] = self.get_queryset().filter(amount__lt=0).extra(select={'month': "to_char(stamp, 'MM' )"}).values('month').annotate(sum=Sum('amount')).order_by()
      context['income'] = self.get_queryset().filter(amount__gte=0).extra(select={'month': "to_char(stamp, 'MM' )"}).values('month').annotate(sum=Sum('amount')).order_by()
      context['total'] = self.get_queryset().extra(select={'month': "to_char(stamp, 'MM' )"}).values('month').annotate(sum=Sum('amount')).order_by()
      context['year'] = self.param_year
      print(context['income'])
      print(context['receivables'])
      context['months'] = ['01','02','03','04','05','06','07','08','09','10','11','12']
      print(context['months'])
      return context