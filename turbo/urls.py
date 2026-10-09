"""
URL configuration for turbo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Internet Magazin API',
        default_version='v1',
        description="Autentifikatsiya: Authorize tugmasi -> 'Token <token_key>'",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


def page(template):
    return TemplateView.as_view(template_name=template)


urlpatterns = [
    path('admin/', admin.site.urls),


    path('api/auth/', include('users.urls')),
    path('api/', include('catalog.urls')),
    path('api/', include('interactions.urls')),
    path('api/', include('cart.urls')),
    path('api/', include('orders.urls')),


    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),


    path('', page('catalog.list.html')),
    path('products/add/', page('catalog.html')),
    path('product/<int:id>/', page('catalog.detail.html')),
    path('cart/', page('cart.html')),
    path('likes/', page('my_likes.html')),
    path('orders/', page('orders.list.html')),
    path('orders/<int:id>/', page('orders.detail.html')),
    path('admin-orders/', page('admin.orders.html')),
    path('login/', page('user.html')),
    path('register/', page('users.base.html')),
    path('profile/', page('user.profile.html')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)