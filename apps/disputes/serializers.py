from rest_framework import serializers
from .models import Dispute

class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = ['id', 'order', 'raised_by', 'reason', 'evidence_text', 'evidence_file', 'status', 'resolution_notes', 'created_at']
        read_only_fields = ['raised_by', 'status', 'resolution_notes']

class DisputeResolveSerializer(serializers.Serializer):
    resolution = serializers.ChoiceField(choices=[
        ('refund', 'Refund Buyer'),
        ('release', 'Release to Seller'),
        ('dismiss', 'Dismiss Dispute')
    ])
    notes = serializers.CharField(required=False)
