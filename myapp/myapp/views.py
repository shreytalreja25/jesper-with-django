from django.http import HttpResponse
from jinja2 import Environment,FileSystemLoader
from jinja2.ext import loopcontrols
from django_jinja_knockout import render_to_response
from django.conf import settings
import pyodbc
import pyjasper

def my_view(request):
    # Connect to SQL server db
    conn = pyodbc.connect(settings.DATABASES['default']['OPTIONS']['driver'] +
                          ';Server=' + settings.DATABASES['default']['HOST'] +
                          ';Database=' + settings.DATABASES['default']['NAME'] +
                          ';UID=' + settings.DATABASES['default']['USER'] +
                          ';PWD=' + settings.DATABASES['default']['PASSWORD'] +
                          ';Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM my_table')
    data = cursor.fetchall()

    pyjasper_path = 'path/to/report.jrxml'
    jasper = pyjasper.PyJasper()
    jasper.compile(pyjasper_path)

    env = Environment(loader = FileSystemLoader('.'))
    env.add_extension(loopcontrols)
    template = env.get_template(pyjasper_path.replace('.jrxml','.html'))
    html = template.render(data=data)
    
    # Return the HTML response with the rendered report
    return HttpResponse(html)