from rest_framework import permissions
from.models import InvestmentAccount

"""
Users with account 2 who have full access"""
class IsCrudAllowed(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.investment_accounts.filter(permission_level='crud').exists()


"""
Users with account 3 who have only "POST" access"""
class IsPostingOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.investment_accounts.filter(permission_level='post').exists()


"""
Users with account 1 who have View only or "GET" access"""
class IsViewOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.investment_accounts.filter(permission_level='view').exists()
