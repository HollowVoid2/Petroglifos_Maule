from pathlib import Path
from datetime import datetime
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Crea un respaldo de la base de datos y la carpeta media.'

    def handle(self, *args, **options):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_root = Path(settings.BACKUP_ROOT)
        backup_root.mkdir(parents=True, exist_ok=True)

        db_path = Path(settings.DATABASES['default']['NAME'])
        db_backup = backup_root / f'db_{timestamp}.sqlite3'
        shutil.copy2(db_path, db_backup)

        media_path = Path(settings.MEDIA_ROOT)
        media_backup = backup_root / f'media_{timestamp}'
        if media_path.exists():
            shutil.copytree(media_path, media_backup)

        self.stdout.write(self.style.SUCCESS('Respaldo creado correctamente.'))
        self.stdout.write(f'BD: {db_backup}')
        self.stdout.write(f'MEDIA: {media_backup}')
