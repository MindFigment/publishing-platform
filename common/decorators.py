from django.http import HttpResponseBadRequest
from django.utils.functional import wraps


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def require_instance_manager(f):
    @wraps(f)
    def wrap(self, *args, **kwargs):
        if self.instance is None:
            raise TypeError(
                f"Can't call {f.__name__} with a non-instance manager")
        return f(self, *args, **kwargs)

    return wrap
