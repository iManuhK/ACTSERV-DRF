from django.contrib import admin
from .models import Transaction, InvestmentAccount
from rangefilter.filters import DateRangeFilter

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'amount', 'date')
    list_filter = (('date', DateRangeFilter), 'user')

    search_fields = ['user__username', 'description']
    ordering = ['date']


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(InvestmentAccount)

