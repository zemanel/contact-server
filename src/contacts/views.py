from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from contacts.datasources import CSVDatasource, DatasourceError
from contacts.forms import ContactListParamsForm

import logging

log = logging.getLogger('contacts.views')


class ListContacts(APIView):
    """
    get:
    Return a list of contacts obtained from an external datasource.
    Sample Response for valid response:

            {
                "data": [
                    {
                        "lastname": "Fox",
                        "zip": "76541",
                        "city": "Killeen",
                        "street": "1859 Clair Street",
                        "image": "/media/male3-512_DIUpMhe.png",
                        "firstname": "Travis"
                    },
                "status": 200
            }

    If the `image_height` or `image_height` HTTP parameters are passed,
    images will be resized and uploaded to media storage.

    HTTP 200 Requests are cached by one second for performance reasons (in case of high
    load, many requests will hit cache and also reduce outgoing server traffic.

    """
    def get(self, request):
        try:
            form = ContactListParamsForm(request.GET)
            if form.is_valid():
                url = settings.CONTACTS_SPREADSHEET_URL
                ds = CSVDatasource(url, form.cleaned_data)
                log.info('Importing CSV from "{}"'.format(url))
                dat = ds.import_csv()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    'status': status.HTTP_400_BAD_REQUEST,
                    'detail': 'Invalid parameters'
                })
        except DatasourceError:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE, data={
                'status': status.HTTP_503_SERVICE_UNAVAILABLE,
                'detail': 'Datasource is not available'
            })
        except Exception as e:
            log.exception(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'detail': 'Server error processing datasource'
            })

        return Response({
            'status': status.HTTP_200_OK,
            'data': dat
        })
