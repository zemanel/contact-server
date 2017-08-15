from django.conf.urls import url
from contacts.views import ListContacts

urlpatterns = [
    url(r'^contacts/', ListContacts.as_view(), name='contacts-list'),
]
