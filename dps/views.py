from django.shortcuts import get_object_or_404
from dps.decorators import dps_result_view
from dps.models import Transaction
from dps.settings import TEMPLATE_ENGINE
from django.template import RequestContext
from django.http import HttpResponseRedirect
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
    transaction.result = pformat(result, width=1)
    transaction.save()

    status_updated = transaction.set_status(Transaction.SUCCESSFUL)
    
    # if we're recurring, we need to save the billing token now.
    content_object = transaction.content_object
    if content_object.is_recurring():
        content_object.set_billing_token(result["DpsBillingId"] or None)

    # callback, if it exists. It may optionally return a url for redirection
    success_url = getattr(content_object,
                          "transaction_succeeded",
                          lambda *args: None)(transaction, True, status_updated)
    
    if success_url:
        # assumed to be a valid url
        return HttpResponseRedirect(success_url)
    else:
        return render_to_response("dps/transaction_success.html", RequestContext(request, {
                    "transaction": transaction}))


@dps_result_view
def transaction_failure(request, token, result=None):
    transaction = get_object_or_404(Transaction.objects.filter(status__in=[Transaction.PROCESSING,
                                                                           Transaction.FAILED]),
                                    secret=token)
    transaction.result = pformat(result, width=1)
    transaction.save()
    
    status_updated = transaction.set_status(Transaction.FAILED)
    
    content_object = transaction.content_object
    
    # callback, if it exists. It may optionally return a url for redirection
    failure_url = getattr(content_object,
                          "transaction_failed",
                          lambda *args: None)(transaction, True, status_updated)
    
    if failure_url:
        # assumed to be a valid url
        return HttpResponseRedirect(failure_url)
    else:
        return render_to_response("dps/transaction_failure.html", RequestContext(request, {
                "transaction": transaction}))

