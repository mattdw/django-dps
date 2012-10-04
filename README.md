DPS payment processing for django. (Almost) completely agnostic about
your models. By default, you never handle credit card details. Handles
one-off and recurring payments.

# Usage:

You'll need `PX(PAY|POST)_USERID` and `PX(PAY|POST)_KEY` in your
settings.py. (`PXPAY_*` for one-off payments, `PXPOST_*` for recurring.)

Then:

`dps.transactions.make_payment(obj, request=None, attrs={})` where:

* obj implements `dps.models.BasicTransactionProtocol` or
  `dps.models.FullTransactionProtocol`.

* request is a request if you intent to make an interactive payment e.g.
  by redirecting the user to the dps page. If it's none, the function
will attempt to find and use a stored billing token and make a
non-interactive recurring payment.

* attrs is a dictionary of PxPay or PxPost request parameters to be
  merged in to the transaction request to DPS.


