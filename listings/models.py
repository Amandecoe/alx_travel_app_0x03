from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Booking(models.Model):
    booking_id = models.PositiveIntegerField(primary_key=True, unique=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings", null=True, blank = True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    total_price = models.PositiveIntegerField()

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        ADMIN = 'admin', 'Admin'

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)



class Review(models.Model):
    review_id = models.PositiveIntegerField(primary_key=True)
    rating = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=200)


class Payment(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    amount = models.PositiveIntegerField()
    tx_ref = models.CharField(max_length=255, null=True, blank=True)         # Chapa transaction reference
    chapa_txn_id = models.CharField(max_length=255, null=True, blank=True)    # Chapa transaction ID
    created_at = models.DateTimeField(auto_now_add=True)

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'

    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)

  
