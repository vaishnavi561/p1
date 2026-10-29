import io
import base64
import traceback
import pytesseract
import cv2
import numpy as np
from PIL import Image
from rapidfuzz import process, fuzz
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..services.llm import call_gemini, structure_with_qwen
from ..services.ocr import MEDICINE_DATABASE

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def scan_prescription_view(request):
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)

    if image_file.size > 5 * 1024 * 1024:
        return Response({"error": "File size exceeds the 5MB limit."}, status=status.HTTP_400_BAD_REQUEST)

    allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
    if image_file.content_type not in allowed_types:
        return Response({"error": "Invalid file type. Only JPEG and PNG images are allowed."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        model_choice = request.data.get('model', 'Gemini')
        api_key = request.data.get('api_key', '')

        if model_choice == 'Gemini':
            if not api_key:
                return Response(
                    {"error": "Please enter your Gemini API key and click Connect."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Local isolated variable processing for Gemini
            img = Image.open(image_file).convert('RGB')
            img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

            prompt = (
                "This is a doctor's prescription. Extract the medicine names with dosage, "
                "frequency and duration, plus any diagnosis or notes. Return a clean, "
                "structured list with name, dose, frequency, and duration clearly separated."
            )
            extracted_text = call_gemini(prompt, api_key, image_b64=encoded_image)
            
            # Atomic return
            return Response({"extracted_text": extracted_text}, status=status.HTTP_200_OK)

        # Local isolated variable processing for Tesseract / Local OCR (P3-03 Atomic Isolation)
        image_file.seek(0)
        img_pil = Image.open(image_file).convert('RGB')
        img_np = np.array(img_pil)

        # 1. Initialize local working variables
        extracted_text_local = ""
        matched_medicines_local = []
        is_ocr_successful = False

        try:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            gray = cv2.resize(gray, (0, 0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            contrast_img = clahe.apply(gray)
            _, thresh = cv2.threshold(contrast_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            custom_config = r'--oem 3 --psm 6'
            extracted_text_local = pytesseract.image_to_string(thresh, config=custom_config)

            for line in extracted_text_local.split('\n'):
                for word in line.split():
                    if len(word) > 3:
                        result = process.extractOne(word, MEDICINE_DATABASE, scorer=fuzz.ratio)
                        if result and result[1] > 75:
                            if result[0] not in matched_medicines_local:
                                matched_medicines_local.append(result[0])
            
            is_ocr_successful = True
        except Exception as ocr_err:
            print(f"OCR half-initialization halted safely: {ocr_err}")
            is_ocr_successful = False

        if not is_ocr_successful:
            return Response(
                {"error": "OCR engine failed to initialize or read the prescription image safely."},
                status=status.HTTP_400_BAD_REQUEST
            )

        final_result = ", ".join(matched_medicines_local) if matched_medicines_local else extracted_text_local.strip()
        if not final_result:
            final_result = "No readable printed text found. Please upload a clear photo or type manually."

        structured = structure_with_qwen(extracted_text_local)

        # Atomic return of fully initialized state
        return Response(
            {
                "extracted_text": structured or final_result,
                "raw_text": extracted_text_local,
                "structured": structured is not None,
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        traceback.print_exc()
        return Response(
            {"error": f"Prescription processing failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )