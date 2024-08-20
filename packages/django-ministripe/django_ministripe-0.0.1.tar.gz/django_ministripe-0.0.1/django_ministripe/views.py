from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django_ministripe import signals
from django.conf import settings
import stripe


class Webhook:
    pass


@csrf_exempt
@require_POST
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.MINISTRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        # TODO: Log warning
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        # TODO: Log warning
        return HttpResponse(status=400)

    # Handle the event
    signal = getattr(signals, event.type.replace('.', '_'))
    if signal:
        signal.send(sender=Webhook, event=event)
    else:
        # TODO: Log warning if event.type does not match any signal?
        pass

    return HttpResponse(status=200)
