from django.core.mail import send_mail
from django.conf import settings

def send_order_notification(order):
    subject = f"Order #{order.id} is {order.status}"

    message = f"""
        Hi {order.user.first_name},

        Your order #{order.id} has been placed successfully.

        Total Amount: {order.grand_total}

        Thank you for shopping with us.
        """,

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.user.email],
        fail_silently=False,
    )
