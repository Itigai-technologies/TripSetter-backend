"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect

def health_check(request):
    """Simple health check endpoint that doesn't require database."""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django backend is running',
        'service': 'Travel Partner API'
    })

def root_redirect(request):
    """Return a simple health payload at root to avoid docs/static issues."""
    return health_check(request)

urlpatterns = [
    # Root URL redirect
    path('', root_redirect, name='root'),
    
    # Admin Honeypot (custom implementation)
    path('admin/honeypot/', include('config.admin_honeypot')),
    
    path('admin/', admin.site.urls),
    
    # Health check endpoint (no database required)
    path('health/', health_check, name='health-check'),
    
    # API URLs
    path('api/auth/', include('apps.authentication.urls')),
    path('api/partner/', include('apps.partner.urls')),
    path('api/common/', include('apps.common.urls')),
    
    # API Documentation (make schema public; serve UI via CDN to avoid static issues)
    path(
        'api/schema/',
        SpectacularAPIView.as_view(permission_classes=[AllowAny]),
        name='schema'
    ),
    path(
        'api/docs/',
        lambda request: HttpResponse(
            """
            <!doctype html>
            <html>
            <head>
              <meta charset="utf-8" />
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <title>API Docs</title>
              <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
              <style>body { margin:0; } .swagger-ui { max-width: 100%; }</style>
            </head>
            <body>
              <div id="swagger"></div>
              <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
              <script>
                window.ui = SwaggerUIBundle({
                  url: '/api/schema/',
                  dom_id: '#swagger',
                  deepLinking: true,
                  presets: [SwaggerUIBundle.presets.apis],
                });
              </script>
            </body>
            </html>
            """,
            content_type='text/html'
        ),
        name='swagger-ui'
    ),
]

# Serve media files in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
