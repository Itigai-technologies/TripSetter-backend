#!/usr/bin/env python3
"""
Test script to verify app.py can be imported correctly.
Run this locally to test: python test_app.py
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import the app
    from app import app
    print("✅ Successfully imported app from app.py")
    print(f"App type: {type(app)}")
    print(f"App object: {app}")
except ImportError as e:
    print(f"❌ Failed to import app: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)

print("✅ All tests passed!")
