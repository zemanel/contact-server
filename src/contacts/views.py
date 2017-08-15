from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from contacts.datasources import CSVDatasource, DatasourceError


class ListContacts(APIView):
    def get(self, request):
        try:
            dat = CSVDatasource.import_csv(settings.CONTACTS_SPREADSHEET_URL)
        except DatasourceError as e:
            return Response(status=500, data={
                'error': str(e)
            })
        return Response(dat)
