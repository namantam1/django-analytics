# analytics.models.py

from django.db import models

from .utils import get_client_ip
from .signals import object_viewed_signal, analytics_signal

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class ObjectViewed(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    ip_address = models.CharField(max_length=120, blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return "%s viewed: %s" % (self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'

class Analytic(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    path = models.CharField(max_length=255, null=True)
    method = models.CharField(max_length=10, null=True)
    params = models.TextField(null=True)
    extra_kwargs = models.TextField(null=True)
    ip_address = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


def analytics_receiver(request, extra_kwargs, *args, **kwargs):
    path = request.path
    ip = None
    method = request.method
    user = request.user
    params = str(dict(request.GET))
    try:
        ip = get_client_ip(request)
    except:
        pass
    analytic = Analytic.objects.create(
        user=user if user.is_authenticated else None,
        path=path,
        ip_address=ip,
        method=method,
        params=params,
        extra_kwargs=str(extra_kwargs),
    )


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    ip_address = None
    user = request.user
    try:
        ip_address = get_client_ip(request)
    except:
        pass
    new_view_instance = ObjectViewed.objects.create(
        user=user if user.is_authenticated else None,
        content_type=c_type,
        object_id=instance.id,
        ip_address=ip_address
    )


object_viewed_signal.connect(object_viewed_receiver)
analytics_signal.connect(analytics_receiver)
