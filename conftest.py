from rest_framework.reverse import reverse


import pytest

@pytest.fixture
def register_data():
    return {"username":"Afrin","password":"12345","email":"afo@gmail.com","phone_number":87557575755,"location":"Pune"}


@pytest.fixture
def user_id(client,register_data):
    user_data=register_data
    url = reverse('register')
    response = client.post(url,user_data,content_type="application/json")

    return response.data.get('data').get('id')