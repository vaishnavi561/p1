from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def family_profile_list_create(request):
    if request.method == 'GET':
        # P2-12: Annotate question_count at the database level
        profiles = FamilyProfile.objects.filter(
            user=request.user, 
            deleted_at__isnull=True
        ).annotate(
            question_count=Count('chats', filter=Q(chats__sender='user'))
        )
        
        # Optional pagination support
        paginator = StandardResultsSetPagination()
        paginated_profiles = paginator.paginate_queryset(profiles, request)
        
        serializer = FamilyProfileSerializer(paginated_profiles, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    # ... POST handling ...
from ..models import FamilyProfile, AuditLog
from ..serializers import FamilyProfileSerializer

def log_audit_event(request, action, details=None):
    """Helper function to record immutable audit logs for healthcare compliance (P0-10)."""
    user = request.user if request.user.is_authenticated else None
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0].strip()
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    AuditLog.objects.create(
        user=user,
        action=action,
        ip_address=ip_address,
        details=details
    )

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def family_profile_list_create(request):
    if request.method == 'GET':
        # P2-05: Filter out soft-deleted profiles so they don't show up in active queries
        profiles = FamilyProfile.objects.filter(user=request.user, deleted_at__isnull=True)
        log_audit_event(request, "VIEW_FAMILY_PROFILE", details=f"User {request.user.username} viewed family profiles.")
        serializer = FamilyProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # P2-05: Count only active (non-soft-deleted) profiles toward the 4-member limit
        user_profile_count = FamilyProfile.objects.filter(user=request.user, deleted_at__isnull=True).count()

        if user_profile_count >= 4:
            return Response(
                {"error": "Maximum limit of 4 family members reached for this account."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = FamilyProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            log_audit_event(request, "CREATE_FAMILY_PROFILE", details=f"User {request.user.username} created a new family profile.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def family_profile_detail(request, pk):
    try:
        # P2-05 & P2-04: Ensure we only lookup active profiles belonging to the logged-in user
        profile = FamilyProfile.objects.get(pk=pk, user=request.user, deleted_at__isnull=True)
    except FamilyProfile.DoesNotExist:
        return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        log_audit_event(request, "VIEW_FAMILY_PROFILE_DETAIL", details=f"User {request.user.username} viewed profile ID {pk}.")
        serializer = FamilyProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        # P2-04: Owner-scoped partial update
        serializer = FamilyProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            log_audit_event(request, "UPDATE_FAMILY_PROFILE", details=f"User {request.user.username} updated profile ID {pk} ({profile.name}).")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        log_audit_event(request, "DELETE_FAMILY_PROFILE", details=f"User {request.user.username} soft-deleted profile ID {pk} ({profile.name}).")
        profile.deleted_at = timezone.now()
        profile.save()
        return Response({"message": "Profile soft-deleted successfully."}, status=status.HTTP_200_OK)