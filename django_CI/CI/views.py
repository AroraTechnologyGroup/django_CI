from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from utils import deploy
import subprocess
from subprocess import PIPE


def stop_site(sitename):
    iis_site = sitename
    kwargs = dict()
    kwargs['stderr'] = PIPE
    kwargs['stdout'] = PIPE
    kwargs['universal_newlines'] = True
    proc = subprocess.Popen('appcmd stop site /site.name:{}'.format(iis_site), **kwargs)
    (std_out, std_err) = proc.communicate()
    return std_out, std_err


def start_site(sitename):
    iis_site = sitename
    kwargs = dict()
    kwargs['stderr'] = PIPE
    kwargs['stdout'] = PIPE
    kwargs['universal_newlines'] = True
    proc = subprocess.Popen('appcmd start site /site.name:{}'.format(iis_site), **kwargs)
    (std_out, std_err) = proc.communicate()
    return std_out, std_err


# Create your views here.
class AroraStaging(APIView):
    """View that calls git pull on the repo"""
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)

    def get(self, request):
        iis_site = 'arora_staging'
        out, err = stop_site(iis_site)
        if not err:
            staging_path = r"C:\inetpub\django_staging\arora"
            x = deploy.pull(app_name="arora", path=staging_path)
        else:
            x = err
        resp = Response(x, headers={'Content-Type': 'application/json', 'Media-Type': 'indent=4'})
        out, err = start_site(iis_site)
        return resp


class RTAAStaging(APIView):
    """View that calls git pull on the repo"""
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)

    def get(self, request):

        iis_site = 'rtaa_gis_staging'
        out, err = stop_site(iis_site)
        if not err:
            staging_path = r"C:\inetpub\django_staging\rtaa_gis"
            x = deploy.pull(app_name="rtaa_gis", path=staging_path)
        else:
            x = err
        resp = Response(x, headers={'Content-Type': 'application/json', 'Media-Type': 'indent=4'})
        out, err = start_site(iis_site)
        return resp
