from django.conf.urls import url
from contacts.views import ListContacts
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^contacts/', cache_page(1)(ListContacts.as_view()), name='contacts-list'),
]
