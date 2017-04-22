from django import template

register = template.Library()

@register.filter
def month_sum_value(month_array, month):
    for d in month_array:
      if str(month) == d['month']:
         return d['sum']
    return '.'

