import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import FamilyProfile

@pytest.mark.django_db
def test_profile_ownership_isolation():
    user1 = User.objects.create_user(username='user1', password='password123')
    user2 = User.objects.create_user(username='user2', password='password123')

    profile1 = FamilyProfile.objects.create(user=user1, name="User1 Family Member")

    client = APIClient()
    client.force_authenticate(user=user2)

    # User 2 should not be able to fetch User 1's profile detail
    response = client.get(f'/api/family-profiles/{profile1.id}/')
    assert response.status_code == 404