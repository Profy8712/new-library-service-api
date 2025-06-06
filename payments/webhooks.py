import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from payments.models import Payment

def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        Payment.objects.filter(session_id=session_id).update(status=Payment.Status.PAID)
    return JsonResponse({"status": "success"})
