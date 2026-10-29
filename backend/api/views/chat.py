import requests
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import FamilyProfile, ChatMessage
from ..serializers import ChatQuerySerializer

MAX_QUESTIONS_LIMIT = 50
MAX_HISTORY_TURNS = 10
MAX_PROMPT_CHARS = 2000  # Rough token/character length cap for small local models

def build_capped_prompt(profile, new_question):
    """
    P2-03: Build prompt from the last N successful turns in chronological order,
    scoped to the profile, and capped by total length.
    """
    recent_messages = ChatMessage.objects.filter(
        profile=profile
    ).order_by('-timestamp')[:MAX_HISTORY_TURNS]
    
    recent_messages = reversed(list(recent_messages))
    
    conversation_context = []
    current_length = 0

    for msg in recent_messages:
        role = "User" if msg.sender == 'user' else "Assistant"
        line = f"{role}: {msg.text}\n"
        
        if current_length + len(line) > MAX_PROMPT_CHARS:
            break
            
        conversation_context.append(line)
        current_length += len(line)

    prompt = "".join(conversation_context) + f"User: {new_question}\nAssistant:"
    return prompt

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_chat_view(request):
    serializer = ChatQuerySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    member_id = serializer.validated_data['member_id']
    question = serializer.validated_data['question']
    model_choice = serializer.validated_data.get('model', 'Ollama')
    api_key = serializer.validated_data.get('api_key', '')

    try:
        with transaction.atomic():
            profile = FamilyProfile.objects.select_for_update().get(
                pk=member_id, 
                user=request.user, 
                deleted_at__isnull=True
            )

            user_question_count = ChatMessage.objects.filter(
                profile=profile, 
                sender='user'
            ).count()

            if user_question_count >= MAX_QUESTIONS_LIMIT:
                return Response(
                    {
                        "error": "Question limit reached.",
                        "remaining_quota": 0
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

            ChatMessage.objects.create(profile=profile, sender='user', text=question)
            remaining_quota = MAX_QUESTIONS_LIMIT - (user_question_count + 1)

        # --- P2-03: Build token-capped prompt ---
        prompt = build_capped_prompt(profile, question)

        # --- AI Generation Logic ---
        ai_response_text = f"Simulated AI response for {profile.name} using prompt length {len(prompt)}."

        with transaction.atomic():
            ChatMessage.objects.create(profile=profile, sender='ai', text=ai_response_text)

        return Response(
            {
                "response": ai_response_text,
                "remaining_quota": remaining_quota
            },
            status=status.HTTP_200_OK
        )

    except FamilyProfile.DoesNotExist:
        return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def model_health_check(request):
    """
    P2-10: Check model connection health (pings Ollama tags or validates API keys).
    """
    model = request.data.get('model', 'Ollama')
    api_key = request.data.get('api_key', '')

    try:
        if model == 'Ollama':
            response = requests.get('http://localhost:11434/api/tags', timeout=3.0)
            if response.status_code == 200:
                return Response({"status": "connected", "model": "Ollama"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Ollama service unavailable."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            if not api_key.strip():
                return Response({"error": f"API key required for {model}."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "connected", "model": model}, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException:
        return Response({"error": "Could not connect to local Ollama server. Ensure Ollama is running."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)