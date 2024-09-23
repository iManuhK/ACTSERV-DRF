from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Transaction, InvestmentAccount
from .serializers import UserSerializer, GroupSerializer, TransactionSerializer, InvestmentAccountSerializer
from .permissions import IsCrudAllowed, IsPostingOnly, IsViewOnly
from django.db.models import Sum


class UserViewSet(viewsets.ModelViewSet):
    """
    A route for viewing and editing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    A route for viewing and editing the Groups .
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class InvestmentAccountViewSet(viewsets.ModelViewSet):
    """
    A route for managing investmeent accounts.
    """
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsCrudAllowed]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class TransactionViewSet(viewsets.ModelViewSet):
    """
    A route for managing transactions.
    Also an Admin endpoint to retrieve the TX for all the users.

    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if  IsCrudAllowed or IsViewOnly:
            return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if  IsCrudAllowed or IsPostingOnly:
            serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        if  IsCrudAllowed:
            serializer.save()


class UserTransactionSummaryViewSet(viewsets.ViewSet):
    """
    Admin endpoint to retrieve the total sum of transactions for all users.
    """
    permission_classes = [permissions.IsAdminUser]
    def list(self, request):
        user_summaries = Transaction.objects.values('user').annotate(total_balance=Sum('amount'))

        summaries = []
        for summary in user_summaries:
            user = User.objects.get(id=summary['user'])
            summaries.append({
                'username': user.username,
                'total_balance': summary['total_balance'] or 0,
            })

        return Response(summaries)
