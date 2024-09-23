from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from django.contrib.auth.models import User, Group
from .models import Transaction, InvestmentAccount
from .views import UserTransactionSummaryViewSet
import datetime
from datetime import timedelta

class TestUserTransactionSummaryViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='testgroup')
        self.group.user_set.add(self.user)

        self.transaction1 = Transaction.objects.create(user=self.user, amount=100, created_at=datetime.datetime.now())
        self.transaction2 = Transaction.objects.create(user=self.user, amount=200, created_at=datetime.datetime.now())

        self.view = UserTransactionSummaryViewSet.as_view({'get': 'list'})
        self.request = self.factory.get('/')
        self.request.user = self.user
    
    def test_list(self):
        response = self.view(self.request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], self.user.username)
        self.assertEqual(response.data[0]['total_balance'], 300)

    def test_list_filtered_by_user(self):
        response = self.view(self.request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], self.user.username)
        self.assertEqual(response.data[0]['total_balance'], 300)
    
    def test_list_with_transactions_grouped_by_day(self):
        # Create transactions with specific days
        transaction1 = Transaction.objects.create(user=self.user, amount=100, created_at=datetime.datetime.now() - timedelta(days=1))
        transaction2 = Transaction.objects.create(user=self.user, amount=200, created_at=datetime.datetime.now() - timedelta(days=2))

        response = self.view(self.request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming response should return 1 summary per user
        self.assertEqual(response.data[0]['username'], self.user.username)
        self.assertEqual(response.data[0]['total_balance'], 300)

        # Check transactions are grouped correctly
        transactions = response.data[0]['transactions']
        self.assertEqual(len(transactions), 2)  # Expecting 2 transactions
        self.assertEqual(transactions[0]['amount'], 100)  # Check amounts
        self.assertEqual(transactions[1]['amount'], 200)

    def test_list_with_transactions_grouped_by_month(self):
        # Create transactions for different months
        transaction1 = Transaction.objects.create(user=self.user, amount=100, created_at=datetime.datetime.now() - timedelta(days=30))
        transaction2 = Transaction.objects.create(user=self.user, amount=200, created_at=datetime.datetime.now() - timedelta(days=60))

        response = self.view(self.request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expecting 1 summary per user
        self.assertEqual(response.data[0]['username'], self.user.username)
        self.assertEqual(response.data[0]['total_balance'], 300)

        # Check transactions are grouped correctly
        transactions = response.data[0]['transactions']
        self.assertEqual(len(transactions), 2)  # Expecting 2 transactions
        self.assertEqual(transactions[0]['amount'], 100)
        self.assertEqual(transactions[1]['amount'], 200)