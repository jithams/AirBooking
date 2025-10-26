from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom User model with approval status for admin workflow.
    """
    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    )

    approval_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        help_text="Admin approval status for the user."
    )

    def is_approved(self):
        """
        Returns True if the user's approval_status is 'Approved'.
        """
        return self.approval_status == self.STATUS_APPROVED

    def __str__(self):
        return f"{self.username} ({self.approval_status})"
