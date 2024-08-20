from django.dispatch import Signal


class WebhookSignalFactory():

    def __new__(self):
        return Signal()


# Checkout
checkout_session_completed = WebhookSignalFactory()