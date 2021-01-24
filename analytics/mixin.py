# analytics.mixins.py

from .signals import object_viewed_signal, analytics_signal

from django.db.models import ObjectDoesNotExist
from django.utils.decorators import method_decorator

from rest_framework import generics

class ObjectViewMixin(generics.RetrieveAPIView):
    def get(self, request, *args,**kwargs):
        print("dispatch ------------>")
        try:
            instance = self.get_object()
        except ObjectDoesNotExist:
            instance = None
        if instance is not None:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return super().get(request, *args, **kwargs)

# @method_decorator
def analytics_view_decorator(function):
    def wrap(request, *args, **kwargs):
        analytics_signal.send(None, request=request, extra_kwargs=kwargs)
        return function(request, *args, **kwargs)

    return wrap
