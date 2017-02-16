from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from utils import deploy
import subprocess
from subprocess import PIPE
import os


def stop_site(sitename):
    iis_site = sitename
    kwargs = dict()
    kwargs['stderr'] = PIPE
    kwargs['stdout'] = PIPE
    kwargs['universal_newlines'] = True
    proc = subprocess.Popen('runas /noprofile /user:GISAPPS\gissetup appcmd stop site /site.name:{}'.format(iis_site), **kwargs)
    (std_out, std_err) = proc.communicate()
    return std_out, std_err


def start_site(sitename):
    iis_site = sitename
    kwargs = dict()
    kwargs['stderr'] = PIPE
    kwargs['stdout'] = PIPE
    kwargs['universal_newlines'] = True
    proc = subprocess.Popen('runas /noprofile /user:GISAPPS\gissetup appcmd start site /site.name:{}'.format(iis_site), **kwargs)
    (std_out, std_err) = proc.communicate()
    return std_out, std_err


# Create your views here.
class AroraStaging(APIView):
    """View that calls git pull on the repo"""
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)

    def get(self, request):
        data = {}
        iis_site = 'arora_staging'
        out, err = stop_site(iis_site)
        data['iis_stop_out'] = out
        data['iis_stop_err'] = err
        if not err:
            staging_path = r"C:\inetpub\django_staging\arora"
            python_path = os.path.join(staging_path, r"venv\scripts\python.exe")
            x = deploy.pull(app_name="arora", staging_path=staging_path, python_path=python_path)
            data.update(x)

        out, err = start_site(iis_site)
        data['iis_start_out'] = out
        data['iis_start_err'] = err
        resp = Response(data, headers={'Content-Type': 'application/json', 'Media-Type': 'indent=4'})
        return resp


class RTAAStaging(APIView):
    """View that calls git pull on the repo"""
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)

    def get(self, request):
        data = {}
        iis_site = 'rtaa_gis_staging'
        out, err = stop_site(iis_site)
        data['iis_stop_out'] = out
        data['iis_stop_err'] = err

        if not err:
            staging_path = r"C:\inetpub\django_staging\rtaa_gis"
            python_path = r"C:\inetpub\Anaconda3\envs\rtaa_gis\python.exe"
            arcpro_path = r"C:\GitHub\arcpro"
            x = deploy.pull_django(app_name="rtaa_gis", staging_path=staging_path, python_path=python_path)
            data.update(x)
            x = deploy.pull_git_repo(arcpro_path)
            data.update(x)

        out, err = start_site(iis_site)
        data['iis_start_out'] = out
        data['iis_start_err'] = err
        resp = Response(data, headers={'Content-Type': 'application/json', 'Media-Type': 'indent=4'})
        return resp


class RTAAProd(APIView):
    """View that calls git pull on the repo"""
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)

    def get(self, request):
        data = {}
        iis_site = 'rtaa_gis_prod'
        out, err = stop_site(iis_site)
        data['iis_stop_out'] = out
        data['iis_stop_err'] = err

        if not err:
            staging_path = r"C:\inetpub\django_prod\rtaa_gis"
            python_path = r"C:\inetpub\Anaconda3\envs\rtaa_gis_prod\python.exe"

            x = deploy.pull(app_name='rtaa_gis', staging_path=staging_path, python_path=python_path)
            data.update(x)

        out, err = start_site(iis_site)
        data['iis_start_out'] = out
        data['iis_start_err'] = err
        resp = Response(data, headers={'Content-Type': 'application/json', 'Media-Type': 'indent=4'})
        return resp