from django.db import models
from django.contrib.auth.models import User, Group

class InvestmentAccount(models.Model):
    code = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_accounts', null=True, blank=True)

    NO_ACCESS = 'default'
    VIEW_ONLY = 'view'
    CRUD_PERMISSIONS = 'crud'
    POST_ONLY = 'post'
    PERMISSION_CHOICES = [
        (NO_ACCESS, 'Default'),
        (VIEW_ONLY, 'View only'),
        (CRUD_PERMISSIONS, 'Full CRUD'),
        (POST_ONLY, 'Post transactions only'),
    ]
    permission_level = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default=NO_ACCESS)

    def __str__(self):
        return f'{self.code} - {self.group.name} - {self.permission_level}'

class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    # user = models.ManytoOneField(User, on_delete=models.SET_NULL, related_name='transactions')

    def __str__(self):
        return f'{self.user.username} - {self.amount} - {self.date}'
