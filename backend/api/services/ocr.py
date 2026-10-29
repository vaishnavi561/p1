import os
import sys
import pytesseract



MEDICINE_DATABASE = [
    "Metformin", "Vitamin D3", "Paracetamol", "Amoxicillin", "Atorvastatin",
    "Omeprazole", "Azithromycin", "Aspirin", "Ibuprofen", "Cetirizine",
    "Pantoprazole", "Amlodipine", "Losartan", "Montelukast", "Levothyroxine",
    "Multivitamin", "Calcium", "Glimepiride", "Telmisartan", "Atorva",
    "Ciprofloxacin", "Doxycycline", "Diclofenac", "Ranitidine", "Prednisolone",
    "Clindamycin", "Metronidazole", "Ondansetron", "Albendazole", "Salbutamol",
    "Budesonide", "Esomeprazole", "Domperidone", "Furosemide", "Spironolactone",
    "Gabapentin", "Pregabalin", "Methylcobalamin", "Folic Acid", "Pantocid",
    "Pan-D", "Shelcal", "Glycomet", "Januvia", "Trajenta", "Ecosprin", "IFA"
]