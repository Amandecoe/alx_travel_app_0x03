from rest_framework import serializers
from .models import Booking, Listing, Payment
class BookingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Booking
    fields = (
      'booking_id',
      'start_date',
      'end_date',
      'total_price',
    )


class ListingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Listing 
    fields = (
      'title',
      'description',
      'price',
      'currency',
      'created_at',
      'is_active',
      'updated_at'
    )

class PaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Payment
    fields = (
      'transaction_id',
      'payment_status',
      'amount'
    )
