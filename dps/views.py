from django.shortcuts import get_object_or_404
from dps.decorators import dps_result_view
from dps.models import Transaction
from dps.settings import TEMPLATE_ENGINE
from django.template import RequestContext
from pprint import pformat

if TEMPLATE_ENGINE in ['jinja', 'jinja2']:
    from coffin.shortcuts import render_to_response
else:
    from django.shortcuts import render_to_response


@dps_result_view
def transaction_success(request, token, result=None):
    transaction = get_object_or_404(Transaction.objects.filter(status__in=[Transaction.PROCESSING,
                                                                          Transaction.SUCCESSFUL]),
                                    secret=token)
    transaction.status = Transaction.SUCCESSFUL
    transaction.result = pformat(result, width=1)
    transaction.save()

    # if we're recurring, we need to save the billing token now.
    content_object = transaction.content_object
    if content_object.is_recurring():
        content_object.set_billing_token(result["DpsBillingId"] or None)

    # callback, if it exists
    getattr(content_object, "transaction_succeeded", lambda t: None)(transaction, True)
    
    return render_to_response("dps/transaction_success.html", RequestContext(request, {
                "transaction": transaction}))


@dps_result_view
def transaction_failure(request, token, result=None):
    transaction = get_object_or_404(Transaction.objects.filter(status__in=[Transaction.PROCESSING,
                                                                           Transaction.FAILED]),
                                    secret=token)
    transaction.status = Transaction.FAILED
    transaction.result = pformat(result, width=1)
    transaction.save()
    
    content_object = transaction.content_object
    getattr(content_object, "transaction_failed", lambda t: None)(transaction, True)
    
    return render_to_response("dps/transaction_failure.html", RequestContext(request, {
                "transaction": transaction}))

