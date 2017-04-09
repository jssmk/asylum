from django import template

register = template.Library()

@register.filter
def keyvalue(month_array, month):
    print("keyvalue "+str(month))
    for d in month_array:
      print(d['month'])
      if month == d['month']:
         print("found "+str(month)+" "+str(d['sum']))
         return d['sum']
    return ''
