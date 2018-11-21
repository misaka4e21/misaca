from rest_framework import viewsets
from rest_framework.response import Response
from misaca_federation.models import Account
from misaca_federation.serializers.account_serializer import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]