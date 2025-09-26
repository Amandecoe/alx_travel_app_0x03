from celery import shared_task
from django.core.mail import send_mail
from .models import Payment

@shared_task
def send_payment_confirmation_email(payment_id):
    try:
        payment = Payment.objects.get(pk = payment_id)
        booking = payment.booking
        user_email = booking.owner.email
        send_mail(
            subject ="Payment Confirmation",
            message = f"Your Payment of {payment.amount} ETB for booking {booking.booking_id} is confirmed.",
            from_email= "noreply@yourdomain.com",
            recipient_list=[user_email]
            )
    except Payment.DoesNotExist:
        pass    