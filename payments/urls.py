from django.urls import path

from . import views

urlpatterns = [
    path("checkout/<int:discharge_id>/", views.create_checkout_session, name="payments-checkout"),
    path("success/", views.payment_success_view, name="payments-success"),
    path("cancel/", views.payment_cancel_view, name="payments-cancel"),
    path("history/", views.payment_history_view, name="payments-history"),
    path("webhook/", views.stripe_webhook, name="stripe-webhook"),
]
