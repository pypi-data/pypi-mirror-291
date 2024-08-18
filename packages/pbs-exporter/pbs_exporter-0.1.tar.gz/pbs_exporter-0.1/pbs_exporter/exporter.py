# pbs_exporter/exporter.py
from distutils import log
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from .pbs_client import PBSClient
import os

import urllib3
import logging
# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PBSExporter:
    def __init__(self, base_url, token):
        self.client = PBSClient(base_url, token)
        self.registry = CollectorRegistry()
        # self.backup_jobs_total = Gauge('pbs_backup_jobs_total', 'Total number of backup jobs', registry=self.registry)
        # self.backup_jobs_running = Gauge('pbs_backup_jobs_running', 'Number of running backup jobs', registry=self.registry)

        self.url_map = Map([
            Rule('/metrics', endpoint='metrics'),
            Rule('/pbs', endpoint='pbs'),
        ])

    def on_metrics(self, request):
        self.client.collect_metrics()
        
        #  response = Response(generate_latest(self.registry), mimetype='text/plain')
        response = Response(generate_latest(), mimetype='text/plain')
        return response

    def on_pbs(self, request):
        # Example implementation for /pbs endpoint
        response_data = '{"message": "This is the PBS endpoint"}'
        response = Response(response_data, mimetype='application/json')
        return response

    def collect_metrics(self):
        data = self.client.get_status()['data']

        self.backup_jobs_total.set(data[0]['avail'])

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, f'on_{endpoint}')(request, **values)
        except Exception as e:
            return Response(str(e), status=404)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(base_url, token):
    return PBSExporter(base_url, token)

def main():
    pbs_base_url = os.getenv('PBS_BASE_URL', 'https://your-proxmox-backup-server')
    pbs_token = os.getenv('PBS_TOKEN', 'your_token')

    app = create_app(pbs_base_url, pbs_token)
    run_simple('0.0.0.0', 8000, app)

if __name__ == '__main__':
    main()