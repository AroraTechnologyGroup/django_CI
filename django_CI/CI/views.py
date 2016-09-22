from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from utils import deploy
import json


# Create your views here.
class AroraStaging(APIView):
    """View that calls git pull on the repo"""
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)

    def get(self, request):
        staging_path = r"C:\inetpub\django_staging\arora"
        x = deploy.pull(app_name="arora", path=staging_path)
        return Response(json.dumps(x))


class RTAAStaging(APIView):
    """View that calls git pull on the repo"""
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)

    def get(self, request):
        staging_path = r"C:\inetpub\django_staging\rtaa_gis"
        x = deploy.pull(app_name="rtaa_gis", path=staging_path)
        return Response(json.dumps(x))
