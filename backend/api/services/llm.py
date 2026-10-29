import base64
import traceback
import requests
from google import genai

def call_gemini(prompt, api_key, image_b64=None):
    """Send a text (and optional image) prompt to Google Gemini using an isolated client instance."""
    client = genai.Client(api_key=api_key.strip())
    
    if image_b64:
        image_bytes = base64.b64decode(image_b64)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, {"mime_type": "image/jpeg", "data": image_bytes}]
        )
    else:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
    return response.text.strip()

def structure_with_qwen(ocr_text):
    prompt = (
        "Below is OCR text from a doctor's prescription. List each medicine on its own "
        "line as: name | dose | frequency | duration. Use ONLY what is in the text. "
        "If something is missing or unclear, write (?). Do not add medicines or "
        "information that is not in the text.\n\n" + ocr_text
    )
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False,
                "keep_alive": 0,
                "options": {"temperature": 0},
            },
            timeout=120,
        )
        if r.status_code == 200:
            return r.json().get("response", "").strip() or None
    except requests.RequestException:
        traceback.print_exc()
    return None