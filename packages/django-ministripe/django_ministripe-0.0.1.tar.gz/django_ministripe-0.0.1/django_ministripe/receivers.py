from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .signals import checkout_session_completed
from .models import StripeCustomer, StripeSubscription


User = get_user_model()


@receiver(checkout_session_completed)
def checkout_session_completed_receiver(**kwargs):
    event = kwargs['event']
    customer_id = event.data['object']['customer']
    subscription_id = event.data['object']['subscription']
    client_reference_id = event.data['object']['client_reference_id']

    user = User.objects.get(id=client_reference_id)

    customer = StripeCustomer.objects.create_or_update(
        id=customer_id,
        user=user
    )
    StripeSubscription.objects.create_or_update(
        id=subscription_id,
        customer=customer,
        status='active'
    )

