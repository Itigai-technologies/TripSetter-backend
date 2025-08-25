"""
Main application entry point for Render deployment.
This file is what Render expects to find for Python web applications.
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
django.setup()

# Import the WSGI application
from django.core.wsgi import get_wsgi_application

# Create the application object that Render expects
app = get_wsgi_application()

# For compatibility with different deployment methods
application = app
