from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = "Create media/static directories if missing (safe no-op on Render)."

    def handle(self, *args, **options):
        dirs = [
            settings.MEDIA_ROOT,
            settings.STATIC_ROOT,
            getattr(settings, 'FILE_UPLOAD_TEMP_DIR', None),
        ]
        created = []
        for d in dirs:
            if not d:
                continue
            try:
                os.makedirs(d, exist_ok=True)
                created.append(str(d))
            except Exception:
                # Avoid failing builds if filesystem is read-only during build
                pass
        if created:
            self.stdout.write(self.style.SUCCESS(f"Ensured directories: {', '.join(created)}"))
        else:
            self.stdout.write("No directories created or already existed.")

