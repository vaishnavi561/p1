# MedLife.ai

MedLife.ai is a full-stack family health management and AI consultation application built with Django REST Framework (backend) and React + Tailwind CSS (frontend). It supports family profile tracking, prescription OCR scanning, and secure local/cloud AI medical consultations.

---

## 🚀 Five-Command Setup

Run these commands in your terminal to set up and start the application locally:

```bash
# 1. Clone and navigate to backend
cd backend

# 2. Create and activate virtual environment & install dependencies
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# 3. Run database migrations
python manage.py migrate

# 4. Start the Django backend server
python manage.py runserver

# 5. In a separate terminal, start the frontend development server
cd frontend && npm install && npm run dev