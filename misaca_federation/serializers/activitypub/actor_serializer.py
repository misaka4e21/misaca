from rest_framework import serializers
from misaca_federation.models import Account
from misaca_federation.helpers.urls.activitypub import *
from django.conf import settings

class EndpointsSerializer(serializers.Serializer):
    sharedInbox = serializers.SerializerMethodField()
    def get_sharedInbox(self, obj):
        return 'https://%s/inbox' % (settings.MISACA_FEDERATION_DOMAIN,)

class ActorSerializer(serializers.ModelSerializer):
    """
    Serializer for local Actor (Account) objects.
    No need to serialize remote Actors.
    """
    id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    preferredUsername = serializers.CharField(source='username')
    name = serializers.CharField(source='display_name')
    inbox = serializers.SerializerMethodField()
    outbox = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    manuallyApprovesFollowers = serializers.BooleanField(source='locked')
    endpoints = EndpointsSerializer(source='*')
    class Meta:
        model = Account
        fields = (
            'id', 'type', 'preferredUsername', 'name', 'url',
            'manuallyApprovesFollowers', 'inbox', 'outbox',
            'followers', 'following', 'endpoints'
        )
    def get_id(self, obj):
        return user_ap_id(obj)
    def get_inbox(self, obj):
        return user_box_uri(obj, 'inbox')
    def get_outbox(self, obj):
        return user_box_uri(obj, 'outbox')
    def get_followers(self, obj):
        return user_box_uri(obj, 'followers')
    def get_following(self, obj):
        return user_box_uri(obj, 'following')
    def get_url(self, obj):
        return user_url(obj)
    def get_type(self, obj):
        if obj.actor_type and obj.actor_type!='':
            return obj.actor_type
        else:
            return ("Service" if obj.is_bot() else "Person")
