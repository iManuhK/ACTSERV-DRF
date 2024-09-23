from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Transaction, InvestmentAccount

class UserSerializer(serializers.ModelSerializer):
    investment_accounts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'investment_accounts']

    def get_investment_accounts(self, obj):
        return [investment_account.permission_level for investment_account in obj.investment_accounts.all()]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'description', 'amount', 'user']
    

class InvestmentAccountSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    class Meta:
        model = InvestmentAccount
        fields = ['url', 'code', 'name', 'users']

    def get_users(self, obj):
        return [user.username for user in obj.user_set.all()]


