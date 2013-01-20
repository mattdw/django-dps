DPS payment processing for django. (Almost) completely agnostic about
your models. By default, you never handle credit card details. Handles
one-off and recurring payments.

# Usage:

You'll need to add a few items in your `settings.py`: `PXPAY_USERID`
and `PXPAY_KEY` for interactive payments and recurring payment setup,
and `PXPOST_USERID` and `PXPOST_KEY` for non-interactive and recurring
billing.

Then, just call this function:

`dps.transactions.make_payment(obj, request=None, attrs={})` where:

* `obj` implements `dps.models.BasicTransactionProtocol` or
  `dps.models.FullTransactionProtocol`.

* `request` is a Django request object or `None`. 

  If you intend to make an interactive payment e.g. by redirecting the
  user to the DPS page, then provide a request. (It's needed to build
  fully-specified URLs for DPS to redirect back to.)
  
  If `request` is `None`, the function will attempt to find and use a
  stored billing token (as described in the protocol implementations
  in `dps/models.py`) and make a non-interactive recurring payment.

* `attrs` is a dictionary of PxPay or PxPost request parameters to be
  merged in to the transaction request to DPS.

  This allows you to do anything, really, as you could override
  default parameters, provide credit-card details directly, specify a
  refund rather than purchase – anything DPS supports.
  
Also supports the [jinja2](http://jinja.pocoo.org/) template engine,
if that is your wish (as it is mine.) Simply add:

    DPS_TEMPLATE_ENGINE = 'jinja' # or 'jinja2', it's not fussy

To your `settings.py`. (This depends on
[coffin](https://github.com/coffin/coffin/) being installed, as I rely
on its `render_to_response`.)
