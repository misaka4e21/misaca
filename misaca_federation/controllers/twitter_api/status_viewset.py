from rest_framework import viewsets
from rest_framework.response import Response
from misaca_federation.models import Status
from misaca_federation.serializers.status_serializer import StatusSerializer

class StatusViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]