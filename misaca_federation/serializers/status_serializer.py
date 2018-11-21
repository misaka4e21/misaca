from rest_framework import serializers
from misaca_federation.models import Status

class StatusSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='text', read_only=True)
    visibility = serializers.CharField(source='get_visibility')

    class Meta:
        model = Status
        fields = ('id', 'in_reply_to_id', 'in_reply_to_account_id',
                  'created_at', 'sensitive', 'spoiler_text', 'visibility', 'language', 'uri', 'url', 'content')