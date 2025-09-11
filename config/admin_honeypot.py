"""
Custom admin honeypot implementation compatible with Django 4.x
This replaces the problematic django-admin-honeypot package
"""

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.urls import path
from django.utils.translation import gettext_lazy as _

class HoneypotAdminSite(AdminSite):
    """Custom admin site that logs all access attempts"""
    
    site_header = _('Site administration')
    site_title = _('Django site admin')
    index_title = _('Site administration')
    
    def has_permission(self, request):
        """Always return False to prevent access"""
        return False
    
    def index(self, request, extra_context=None):
        """Log the access attempt and return a fake admin page"""
        # Log the access attempt (you can implement logging here)
        print(f"Honeypot accessed by: {request.META.get('REMOTE_ADDR', 'Unknown')}")
        
        # Return a fake admin page
        return HttpResponse(
            f"""
            <html>
            <head><title>Site administration | Django site admin</title></head>
            <body>
                <h1>Site administration</h1>
                <p>Welcome to Django site admin.</p>
                <p>This is a honeypot - all access attempts are logged.</p>
            </body>
            </html>
            """,
            content_type='text/html'
        )

# Create the honeypot admin site
honeypot_admin = HoneypotAdminSite(name='honeypot_admin')

# Register a fake user model
honeypot_admin.register(User, UserAdmin)

# URL patterns for the honeypot
honeypot_urlpatterns = [
    path('', honeypot_admin.urls),
]

# Expose standard urlpatterns variable so Django include() can import this module
urlpatterns = honeypot_urlpatterns
