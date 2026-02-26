from django.db import models
from django.contrib.auth import get_user_model
from apps.orders.models import Order

User = get_user_model()

class Dispute(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        RESOLVED_REFUND = 'resolved_refund', 'Resolved (Refund)'
        RESOLVED_RELEASE = 'resolved_release', 'Resolved (Release Funds)'
        DISMISSED = 'dismissed', 'Dismissed'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='disputes')
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='raised_disputes')
    reason = models.TextField()
    evidence_text = models.TextField(blank=True, help_text="Description of the issue")
    evidence_file = models.FileField(upload_to='disputes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dispute #{self.id} for Order #{self.order_id}"
