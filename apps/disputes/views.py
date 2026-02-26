from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from .models import Dispute
from .serializers import DisputeSerializer, DisputeResolveSerializer

class DisputeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DisputeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role == 'admin':
            return Dispute.objects.all()
        return Dispute.objects.filter(raised_by=user)

    def perform_create(self, serializer):
        serializer.save(raised_by=self.request.user)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def resolve(self, request, pk=None):
        dispute = self.get_object()
        serializer = DisputeResolveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action = serializer.validated_data['resolution']
        notes = serializer.validated_data.get('notes', '')
        
        if action == 'refund':
            dispute.status = Dispute.Status.RESOLVED_REFUND
            # Trigger Refund Logic
        elif action == 'release':
            dispute.status = Dispute.Status.RESOLVED_RELEASE
            # Trigger Release Logic
        elif action == 'dismiss':
            dispute.status = Dispute.Status.DISMISSED
            
        dispute.resolution_notes = notes
        dispute.save()
        
        return Response({'status': 'resolved', 'outcome': dispute.status})
