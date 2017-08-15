import pytest
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@pytest.fixture
def basic_user():
    return UserModel.objects.create_user('user1',
                                         email='email@localhost',
                                         password='secret')
