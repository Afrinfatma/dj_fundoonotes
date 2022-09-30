import pytest

from rest_framework.reverse import reverse


class TestUser:
    @pytest.mark.django_db
    def test_user_registration(self, client, register_data):
        """
             Testing user if registered should return 201 status code
             """
        data = register_data
        url = reverse('register')
        response = client.post(url, data,content_type="application/json")

        assert response.status_code == 201

    @pytest.mark.django_db
    def test_user_login(self, client, register_data):
        """
             Testing user if logged in should return 202 status code
             """
        data = register_data
        url = reverse('register')
        response = client.post(url, data,content_type="application/json")
        assert response.status_code == 201
        url = reverse('login')
        login_data = {"username": "Afrin", "password": "12345", "email": "afo@gmail.com"}
        response = client.post(url, login_data, content_type="application/json")
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_user_invalid_login(self, client, register_data):
        """
             Testing user if invalid login details should return 400 status code
             """
        data = register_data
        url = reverse('register')
        response = client.post(url, data,content_type="application/json")
        assert response.status_code == 201
        url = reverse('login')
        login_data = {"username": "Fatma", "password": "12345", "email": "afo@gmail.com"}
        response = client.post(url, login_data,content_type="application/json")

        assert response.status_code == 400

    @pytest.mark.django_db
    def test_invalid_userpassword(self, client, register_data):
        """
             Testing user if invalid user password given,should return 400 status code
             """
        data = register_data
        url = reverse('register')
        response = client.post(url, data,content_type="application/json")
        assert response.status_code == 201
        url = reverse('login')
        login_data = {"username": "Afrin", "password": "rgbnh", "email": "afo@gmail.com"}
        response = client.post(url, login_data,content_type="application/json")

        assert response.status_code == 400
