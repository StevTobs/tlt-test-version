import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from core.models import Province, Amphure, Tambon

class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Invalid JSON: {e}"))
            return

        for province_data in data:
            province, created = Province.objects.update_or_create(
                id=province_data['id'],
                defaults={
                    'name_th': province_data['name_th'],
                    'name_en': province_data['name_en'],
                    'geography_id': province_data['geography_id'],
                    'created_at': parse_datetime(province_data['created_at']),
                    'updated_at': parse_datetime(province_data['updated_at']),
                    'deleted_at': parse_datetime(province_data['deleted_at']) if province_data['deleted_at'] else None,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Province: {province.name_en}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated Province: {province.name_en}"))

            for amphure_data in province_data.get('amphure', []):
                amphure, created = Amphure.objects.update_or_create(
                    id=amphure_data['id'],
                    defaults={
                        'name_th': amphure_data['name_th'],
                        'name_en': amphure_data['name_en'],
                        'province': province,
                        'created_at': parse_datetime(amphure_data['created_at']),
                        'updated_at': parse_datetime(amphure_data['updated_at']),
                        'deleted_at': parse_datetime(amphure_data['deleted_at']) if amphure_data['deleted_at'] else None,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"  Created Amphure: {amphure.name_en}"))
                else:
                    self.stdout.write(self.style.WARNING(f"  Updated Amphure: {amphure.name_en}"))

                for tambon_data in amphure_data.get('tambon', []):
                    tambon, created = Tambon.objects.update_or_create(
                        id=tambon_data['id'],
                        defaults={
                            'zip_code': tambon_data['zip_code'],
                            'name_th': tambon_data['name_th'],
                            'name_en': tambon_data['name_en'],
                            'amphure': amphure,
                            'lat': tambon_data.get('lat'),
                            'lng': tambon_data.get('lng'),
                            'created_at': parse_datetime(tambon_data['created_at']),
                            'updated_at': parse_datetime(tambon_data['updated_at']),
                            'deleted_at': parse_datetime(tambon_data['deleted_at']) if tambon_data['deleted_at'] else None,
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"    Created Tambon: {tambon.name_en}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"    Updated Tambon: {tambon.name_en}"))

        self.stdout.write(self.style.SUCCESS("Data loading completed successfully."))
