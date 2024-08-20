from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
import stripe


stripe.api_key = settings.MINISTRIPE_SECRET_KEY
User = get_user_model()


class StripeCustomer(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stripe_customer')

    def get_billing_portal_session(self):
        return stripe.billing_portal.Session.create(
            customer=self.id
        )


class StripeSubscription(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    customer = models.OneToOneField(StripeCustomer, on_delete=models.CASCADE, related_name='subscription')
    status = models.CharField(max_length=255)

    def sync(self):
        """
        Sync subscription status with Stripe
        """
        subscription = stripe.Subscription.retrieve(self.id)
        self.status = subscription.status
        self.save()
