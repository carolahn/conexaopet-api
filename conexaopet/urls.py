from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ConexaoPet API",
        default_version='v1',
        description="Documentação da ConexaoPet API",
        contact=openapi.Contact(email="ahncarolina@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/', include('cupom.urls')),
    path('api/', include('pet.urls')),
    path('api/', include('address.urls')),
    path('api/', include('event.urls')),
    path('api/', include('favorite_pet.urls')),
    path('api/', include('favorite_event.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# urlpatterns += [
#     re_path(r'^api/media/cupom_images/(?P<path>.*)$', serve, {'document_root': settings.CUPOM_IMAGES_DIR}),
#     re_path(r'^api/media/event_images/(?P<path>.*)$', serve, {'document_root': settings.EVENT_IMAGES_DIR}),
#     re_path(r'^api/media/pet_images/(?P<path>.*)$', serve, {'document_root': settings.PET_IMAGES_DIR}),
#     re_path(r'^api/media/profile_images/(?P<path>.*)$', serve, {'document_root': settings.PROFILE_IMAGES_DIR}),
# ]

# Para o servidor local usar:
# urlpatterns += static(settings.CUPOM_IMAGES_URL, document_root=settings.CUPOM_IMAGES_DIR)
# urlpatterns += static(settings.EVENT_IMAGES_URL, document_root=settings.EVENT_IMAGES_DIR)
# urlpatterns += static(settings.PET_IMAGES_URL, document_root=settings.PET_IMAGES_DIR)
# urlpatterns += static(settings.PROFILE_IMAGES_URL, document_root=settings.PROFILE_IMAGES_DIR)

# Para servir pelo nginx:
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)