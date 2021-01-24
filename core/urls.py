# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

from product.views import ProductDetail
from analytics.mixin import analytics_view_decorator

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("product/<pk>/", analytics_view_decorator(ProductDetail.as_view()), name="product_detail"),
    path("", include("authentication.urls")), # Auth routes - login / register
    path("", include("app.urls")),             # UI Kits Html files
]


    
