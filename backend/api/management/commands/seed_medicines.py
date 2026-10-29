from django.core.management.base import BaseCommand
from api.models import Medicine

STARTER_MEDICINES = [
    {"name": "Metformin", "generic_name": "Metformin", "brand_name": "Glucophage", "category": "Diabetes"},
    {"name": "Glycomet", "generic_name": "Metformin", "brand_name": "Glycomet", "category": "Diabetes"},
    {"name": "Januvia", "generic_name": "Sitagliptin", "brand_name": "Januvia", "category": "Diabetes"},
    {"name": "Trajenta", "generic_name": "Linagliptin", "brand_name": "Trajenta", "category": "Diabetes"},
    {"name": "Vitamin D3", "generic_name": "Cholecalciferol", "brand_name": "Vitamin D3", "category": "Vitamin"},
    {"name": "Paracetamol", "generic_name": "Paracetamol", "brand_name": "Crocin / Calpol", "category": "Analgesic"},
    {"name": "Amoxicillin", "generic_name": "Amoxicillin", "brand_name": "Amoxil", "category": "Antibiotic"},
    {"name": "Atorvastatin", "generic_name": "Atorvastatin", "brand_name": "Lipitor", "category": "Statin"},
    {"name": "Atorva", "generic_name": "Atorvastatin", "brand_name": "Atorva", "category": "Statin"},
    {"name": "Omeprazole", "generic_name": "Omeprazole", "brand_name": "Prilosec", "category": "Antacid"},
    {"name": "Pantocid", "generic_name": "Pantoprazole", "brand_name": "Pantocid", "category": "Antacid"},
    {"name": "Pan-D", "generic_name": "Pantoprazole + Domperidone", "brand_name": "Pan-D", "category": "Antacid"},
    {"name": "Shelcal", "generic_name": "Calcium + Vitamin D3", "brand_name": "Shelcal", "category": "Supplement"},
    {"name": "Ecosprin", "generic_name": "Aspirin", "brand_name": "Ecosprin", "category": "Blood Thinner"},
    {"name": "Azithromycin", "generic_name": "Azithromycin", "brand_name": "Zithromax", "category": "Antibiotic"},
    {"name": "Aspirin", "generic_name": "Aspirin", "brand_name": "Bayer", "category": "Blood Thinner"},
    {"name": "Ibuprofen", "generic_name": "Ibuprofen", "brand_name": "Advil", "category": "NSAID"},
    {"name": "Cetirizine", "generic_name": "Cetirizine", "brand_name": "Zyrtec", "category": "Antihistamine"},
    {"name": "Pantoprazole", "generic_name": "Pantoprazole", "brand_name": "Protonix", "category": "Antacid"},
    {"name": "Amlodipine", "generic_name": "Amlodipine", "brand_name": "Norvasc", "category": "Blood Pressure"},
    {"name": "Losartan", "generic_name": "Losartan", "brand_name": "Cozaar", "category": "Blood Pressure"},
    {"name": "Montelukast", "generic_name": "Montelukast", "brand_name": "Singulair", "category": "Respiratory"},
    {"name": "Levothyroxine", "generic_name": "Levothyroxine", "brand_name": "Synthroid", "category": "Thyroid"}
]

class Command(BaseCommand):
    help = 'Seeds the Medicine database table with STARTER_MEDICINES and brand-to-generic mappings (P14).'

    def handle(self, *args, **options):
        count = 0
        for med_data in STARTER_MEDICINES:
            obj, created = Medicine.objects.update_or_create(
                name=med_data['name'],
                defaults={
                    'generic_name': med_data['generic_name'],
                    'brand_name': med_data['brand_name'],
                    'category': med_data['category']
                }
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} new medicines (Total: {len(STARTER_MEDICINES)}) into the database."))