from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


def rate_limit_decorater(rate='10/m'):
    """Reusable decorater factory for rate limiting any view"""
    def decorater(view_class):
        view_class.dispatch=method_decorator(
            ratelimit(key='user_or_ip',rate=rate,method='ALL')
            )(view_class.dispatch)
        return view_class
    return decorater