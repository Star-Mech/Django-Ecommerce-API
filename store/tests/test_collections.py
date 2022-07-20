from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import pytest
from model_bakery import baker

from store.models import Collection, Product


@pytest.fixture
def create_collection(api_client):# can't pass the collection parameter directly to this line. Hence an inner function is created
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)

    return do_create_collection


@pytest.mark.django_db # To allow DataBase access
class TestCreateCollection:
    def test_if_user_anonymous_returns_401(self, create_collection):
        # client = APIClient()
        response = create_collection({'title': 'a'})
        # response = api_client.post('/store/collections/', {'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_returns_403(self, create_collection, authenticate_user):
        # client = APIClient()
        authenticate_user(is_staff=False) # Not admin User But a registered User


        response = create_collection({'title': 'a'})


        # client.force_authenticate(user={})
        # response = client.post('/store/collections/', {'title': 'a'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_invalid_returns_409(self, create_collection, authenticate_user):
        # client = APIClient()
        # client.force_authenticate(user=User(is_staff=True))
        # response = client.post('/store/collections/', {'title': ''}) # title is empty. invalid data
        authenticate_user(is_staff=True)
        response = create_collection({'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_valid_returns_201(self, create_collection, authenticate_user):
        # client = APIClient()
        # client.force_authenticate(user=User(is_staff=True))
        # response = client.post('/store/collections/', {'title': 'as'})
        authenticate_user(is_staff=True)

        response = create_collection({'title': 'as'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0 is not None


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        #Arrange
        # Collection.objects.create(title='Col76')
        collection = baker.make(Collection) # Model baker will automatically create a collection
        # baker.make(Product, collection=collection, _quantity=10)# if collection not specified, new willl be created for every product

        #Act
        response = api_client.get(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK # Return code is 200
        # assert response.data['id'] == collection.id # The returned data is the correcet data
        print(response.data)
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0,   # number of products in the collection, this annotated to response in CollectionViewSet
        }
    def test_if_collection_list_returns_200(self, api_client):
        #Arrange

        #Act
        response = api_client.get(f'/store/collections/')
        assert response.status_code == status.HTTP_200_OK # Return code is 200
