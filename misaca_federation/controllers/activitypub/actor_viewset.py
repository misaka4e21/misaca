from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from misaca_federation.models import Account
from misaca_federation.parsers import *
from misaca_federation.serializers.activitypub.actor_serializer import ActorSerializer
from misaca_federation.renderers import ActivityStreamsRenderer, ActivityStreamsLDJSONRenderer

class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    base_name='user'
    renderer_classes = (ActivityStreamsRenderer,ActivityStreamsLDJSONRenderer)
    parser_classes = (ActivityStreamsParser, JSONParser)

    queryset = Account.objects.filter(domain=None)
    serializer_class = ActorSerializer
    lookup_field = 'username'
    lookup_value_regex = r'[^@\/]+'

    @action(detail=True)
    def inbox(self, request, username=None):
        return Response({username: username})
    #permission_classes = [IsAccountAdminOrReadOnly]
#    def retrieve(self, request, pk=None):
#        queryset = Account.objects.all()
#        actor = get_object_or_404(queryset, username=pk, domain=None)
#        serializer = self.serializer_class(actor)
#        return Response(serializer.data)
