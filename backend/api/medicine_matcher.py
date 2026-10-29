from .models import Medicine
from rapidfuzz import process, fuzz

def get_medicine_database():
    """Fetch all medicine names from the unified Medicine table (P14)."""
    try:
        medicines = list(Medicine.objects.values_list('name', flat=True))
        if medicines:
            return medicines
    except Exception:
        pass

    return [
        "Metformin", "Glycomet", "Januvia", "Trajenta", "Vitamin D3", 
        "Paracetamol", "Amoxicillin", "Atorvastatin", "Atorva", "Omeprazole", 
        "Pantocid", "Pan-D", "Shelcal", "Ecosprin", "Azithromycin", "Aspirin", 
        "Ibuprofen", "Cetirizine", "Pantoprazole", "Amlodipine", "Losartan", 
        "Montelukast", "Levothyroxine"
    ]

def match_medicine(word):
    database = get_medicine_database()
    if not database:
        return None
    result = process.extractOne(word, database, scorer=fuzz.ratio)
    if result and result[1] > 75:
        return result[0]
    return None

def parse_prescription_lines(extracted_text):
    matched_medicines = []
    database = get_medicine_database()
    for line in extracted_text.split('\n'):
        for word in line.split():
            if len(word) > 3:
                result = process.extractOne(word, database, scorer=fuzz.ratio)
                if result and result[1] > 75:
                    if result[0] not in matched_medicines:
                        matched_medicines.append(result[0])
    return matched_medicines