import cgitb
import subprocess
from subprocess import PIPE
from django.core.mail import send_mail
from django.core import mail
import os, sys
cgitb.enable()


def pull(app_name, path):
    kwargs = dict()
    kwargs['cwd'] = path
    kwargs['stderr'] = PIPE
    kwargs['stdout'] = PIPE
    kwargs['universal_newlines'] = True
    git_cmd = "git pull"
    proc = subprocess.Popen(git_cmd, **kwargs)
    (std_out, std_err) = proc.communicate()

    BASE_DIR = os.path.join(path, app_name)
    sys.path.append(BASE_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = '{}.settings'.format(app_name)

    kwargs = dict()
    kwargs['stderr'] = PIPE
    kwargs['stdout'] = PIPE
    kwargs['universal_newlines'] = True
    python_path = os.path.join(BASE_DIR, r"venv\scripts\python.exe")
    manage_script = os.path.join(BASE_DIR, "manage.py")
    proc = subprocess.Popen("{} {} collectstatic --no-input --settings={}.settings".format(python_path, manage_script,
                                                                                             app_name), **kwargs)
    (out, err) = proc.communicate()

    connection = mail.get_connection()
    connection.open()
    report_string = "std_out: {} \n std_err: {} \n collectstatic: {} \n err: {}".format(std_out, std_err, out, err)
    send_mail(
        "Deploy {} to Staging".format(app_name),
        report_string,
        "rhughes@aroraengineers.com",
        ["richardh522@gmail.com"],
        fail_silently=False,
    )
    connection.close()

    return report_string
