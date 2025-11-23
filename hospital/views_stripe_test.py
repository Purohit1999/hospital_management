from django.http import JsonResponse
from django.conf import settings


def stripe_keys_test(request):
    return JsonResponse({
        'publishable_key_loaded': settings.STRIPE_PUBLISHABLE_KEY is not None,
        'secret_key_loaded': settings.STRIPE_SECRET_KEY is not None
    })

