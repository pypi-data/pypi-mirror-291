from django.contrib import admin
from django_ministripe.models import StripeCustomer, StripeSubscription


admin.site.register(StripeCustomer)
admin.site.register(StripeSubscription)
