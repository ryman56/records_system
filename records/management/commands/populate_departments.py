# records/management/commands/populate_departments.py

from django.core.management.base import BaseCommand
from records.models import Department

class Command(BaseCommand):
    help = 'Populate initial departments in the database'

    def handle(self, *args, **kwargs):
        departments = [
            {"name": "Information Technology (IT) Department", "description": "Handles all IT-related activities."},
            {"name": "Telecommunications Department", "description": "Manages telecommunications services."},
            {"name": "Cybersecurity Department", "description": "Ensures the security of digital assets."},
            {"name": "Digital Services Department", "description": "Manages digital service offerings."},
            {"name": "Policy and Planning Department", "description": "Handles policy-making and strategic planning."},
            {"name": "Research and Development (R&D) Department", "description": "Focuses on innovation and research."},
            {"name": "Administration and Finance Department", "description": "Manages administrative and financial tasks."},
            {"name": "Public Relations and Communications Department", "description": "Handles public relations and communications."},
            {"name": "E-Government Department", "description": "Manages e-government services."},
            {"name": "Data Management and Analytics Department", "description": "Handles data analytics and management."},
            {"name": "Regulatory and Compliance Department", "description": "Ensures regulatory compliance."},
            {"name": "Human Resources Department", "description": "Manages HR-related activities."}
        ]

        for dept in departments:
            Department.objects.get_or_create(name=dept['name'], defaults={'description': dept['description']})
            self.stdout.write(self.style.SUCCESS(f"Department '{dept['name']}' created or already exists."))
