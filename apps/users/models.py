from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        SELLER = 'seller', _('Seller')
        BUYER = 'buyer', _('Buyer')

    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.BUYER,
    )

    
    
    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return self.username

    def is_seller(self):
        return self.role == self.Role.SELLER

    def is_buyer(self):
        return self.role == self.Role.BUYER


class Store(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='store',
        limit_choices_to={'role': User.Role.SELLER}
    )
    store_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    store_logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    store_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.store_name:
            original_slug = slugify(self.store_name)
            self.slug = original_slug
            counter = 1
            while Store.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.store_name
