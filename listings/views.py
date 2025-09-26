from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
from django.conf import settings
import uuid
from rest_framework.permissions import IsAuthenticated


CHAPA_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_VERIFY_URL = "https://api.chapa.co/v1/transaction/verify/"

class listingViewSet(viewsets.ModelViewSet):
  queryset = Listing.objects.all()
  serializer_class = ListingSerializer
  permission_classes = [IsAuthenticated]
  def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer

class PaymentViewSet(viewsets.ModelViewSet):
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer

class InitiatePaymentView(APIView):
    def post(self, request):
        booking_id = request.data.get("booking_id")
        amount = request.data.get("amount")

        # Validate input
        if not booking_id or not amount:
            return Response({"error": "booking_id and amount are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Fetch the booking
        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"},
                            status=status.HTTP_404_NOT_FOUND)

        # Ensure booking has a listing
        if not booking.listing:
            return Response({"error": "Booking has no associated listing"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Ensure listing has an owner with email
        if not booking.listing.owner or not booking.listing.owner.email:
            return Response({"error": "Listing owner is missing or has no email"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Generate unique transaction reference
        tx_ref = str(uuid.uuid4())

        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": booking.listing.owner.email,
            "first_name": booking.listing.owner.first_name,
            "last_name": booking.listing.owner.last_name,
            "tx_ref": tx_ref
        }

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        # Call Chapa API
        try:
            response = requests.post(CHAPA_URL, json=payload, headers=headers)
            response_data = response.json()
        except Exception as e:
            return Response({"error": f"Chapa API request failed: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Handle Chapa response
        if response_data.get("status") == "success":
            # Save payment as pending
            Payment.objects.create(
                booking=booking,
                amount=amount,
                tx_ref=tx_ref,
                chapa_txn_id=response_data["data"]["checkout_url"],  # Chapa checkout URL
                status=Payment.payment_status.PENDING
            )
            return Response(
                {"checkout_url": response_data["data"]["checkout_url"], "tx_ref": tx_ref},
                status=status.HTTP_200_OK
            )
        else:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyPaymentView(APIView):
  def post(self, request):
    tx_ref = request.data.get("tx_ref")
    try:
      payment = Payment.objects.get(tx_ref = tx_ref)    
    except Payment.DoesNotExist:
      return Response({"error": "Payment not found"}, status = status.HTTP_404_NOT_FOUND)  
    headers = {
      "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    }

    #call chapa verify api
    response = request.get(f"{CHAPA_VERIFY_URL}{tx_ref}", headers = headers)
    response_data = response.json()
    if response_data.get("status") == "success":
      chapa_status = response_data["data"]["status"]

      #update payment status in our DB
      if chapa_status.lower() == "successful":
        payment.status = Payment.payment_status.CONFIRMED
      else:
        payment.status = Payment.payment_status.PENDING

      payment.save()

      return Response({
        "tx_ref":tx_ref,
        "payment_status":payment.status,
        "chapa_status":chapa_status
      }, status=status.HTTP_200_OK)
    else:
      return Response({"error":response_data}, status = status.HTTP_400_BAD_REQUEST)    