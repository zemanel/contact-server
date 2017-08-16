import pytest
import requests_mock
from django.conf import settings
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db()
def test_list_requires_authentication():
    api_client = APIClient()
    url = reverse('contacts-list')
    r = api_client.get(url)
    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
@pytest.mark.usefixtures('basic_user')
def test_should_list_contacts():
    with requests_mock.mock() as m:
        m.get(settings.CONTACTS_SPREADSHEET_URL, text='a,b\n1,2')

        api_client = APIClient()
        api_client.login(username='user1', password='secret')

        url = reverse('contacts-list')
        r = api_client.get(url)
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {
            'data': [
                {'a': '1', 'b': '2'}
            ],
            'status': 200
        }
