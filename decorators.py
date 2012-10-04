from dps.transactions import get_interactive_result

def dps_result_view(func):
    """Calls the inner func with an additional 'result' kwarg, which
    is an xml document of the DPS response/result.""" 
    def _inner(request, *args, **kwargs):
        result_token = request.GET.get("result")
        kwargs["result"] = get_interactive_result(result_token)
        return func(request, *args, **kwargs)

    _inner.__name__ = func.__name__
    _inner.__doc__ = func.__doc__
    _inner.__module__ = func.__module__
    return _inner
