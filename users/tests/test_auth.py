import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    url = reverse("user-register")
    data = {
        "email": "user1@example.com",
        "first_name": "First",
        "last_name": "Last",
        "password": "strongpassword"
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert User.objects.filter(email="user1@example.com").exists()


@pytest.mark.django_db
def test_jwt_token_obtain_and_auth():
    password = "pw12345678"
    user = User.objects.create_user(
        email="user2@example.com", first_name="Fn", last_name="Ln", password=password
    )
    client = APIClient()

    url = reverse("token-obtain")
    # By default, SimpleJWT expects "username", not "email". If you have custom serializer, change to "email"
    response = client.post(url, {"username": user.email, "password": password})
    assert response.status_code == 200
    assert "access" in response.data

    access_token = response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    profile_url = reverse("user-profile")
    response2 = client.get(profile_url)
    assert response2.status_code == 200
    assert response2.data["email"] == user.email
