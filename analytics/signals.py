# analytics.signals.py 

from django.dispatch import Signal

object_viewed_signal = Signal(providing_args=['instance', 'request'])
analytics_signal = Signal(providing_args=['request', 'extra_kwargs'])