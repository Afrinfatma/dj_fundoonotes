import pytest
from rest_framework.reverse import reverse


"""
* By default python prevents database access, To enable the access from the database,
    we are using @pytest.mark.django_db decorator
* we are specifying duplicates in every function, to remove duplicacy  
    (voilating dry concept) we are creating a fixtures in conftest.py, this fixtures 
    are automatically loads without explicitly import this module
* each time pytest is running in every function, it will treat database as blank
"""


class TestNotes:

    @pytest.mark.django_db
    def test_created_notes(self, client, user_id):
        """
              Testing notes if created should return 201 status code
              """
        note_data = {"title": "Project C", "description": "Project C details", "user_id": user_id}
        url = reverse('note')

        response = client.post(url, note_data, content_type="application/json")

        assert response.status_code == 201

    @pytest.mark.django_db
    def test_notes_retrieved(self, client, user_id):
        """
              Testing notes if retrieved successfully should return 200 status code
              """
        note_data = {"title": "Project C", "description": "Project C details", "user_id": user_id}
        url = reverse('note')

        response = client.post(url, note_data, content_type="application/json")

        assert response.status_code == 201

        data = {"user_id": user_id}

        get_response = client.get(url, data, content_type="application/json")

        assert get_response.status_code == 200

    @pytest.mark.django_db
    def test_updated_notes(self, client, user_id):
        """
              Testing notes if updated successfully  should return 202 status code
              """
        note_data = {"title": "Project C", "description": "Project C details", "user_id": user_id}
        url = reverse('note')

        response = client.post(url, note_data, content_type="application/json")

        assert response.status_code == 201
        assert response.data.get('data').get('title') == "Project C"
        note_id = response.data.get('data').get('id')
        data = {"id": note_id, 'title': 'Project C', 'description': 'Project C details', 'user_id': user_id}
        put_response = client.put(url, data, content_type="application/json")
        assert put_response.status_code == 202

    @pytest.mark.django_db
    def test_deleted_notes(self, client, user_id):
        """
              Testing notes if deleted successfully  should return 204 status code
              """
        note_data = {"title": "Project C", "description": "Project C details", "user_id": user_id}
        url = reverse('note')

        response = client.post(url, note_data, content_type="application/json")

        assert response.status_code == 201
        note_id = response.data.get('data').get('id')
        data = {"id": note_id, 'user_id': user_id}
        del_response =client.delete(url,data,content_type="application/json")
        assert del_response.status_code == 204