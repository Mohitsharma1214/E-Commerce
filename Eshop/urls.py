from django.contrib import admin
from django.urls import path  , include
from django.conf.urls.static import static
from . import settings
from django.conf.urls import handler404
from store.views.pagenf import custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('store.urls')),
     path('i18n/', include('django.conf.urls.i18n')),
    
    # Admin URL patterns
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# handler404 = custom_404_view     