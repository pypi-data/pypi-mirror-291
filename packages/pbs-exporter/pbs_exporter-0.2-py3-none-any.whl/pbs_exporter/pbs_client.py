# pbs_exporter/pbs_client.py

# import requests
# import logging

# PROM_NAMESPACE = "pbs"
# VERSION_API = "/api2/json/version"
# DATASTORE_USAGE_API = "/api2/json/status/datastore-usage"
# DATASTORE_API = "/api2/json/admin/datastore"
# NODE_API = "/api2/json/nodes"

# class PBSClient:
#     def __init__(self, base_url, token):
#         self.base_url = base_url
#         self.headers = {'Authorization': f'PBSAPIToken={token}'}
#         logging.info(self.base_url)
#         logging.info(self.headers)

#     def get_status(self):
#         url = f"{self.base_url}/api2/json/status/datastore-usage"
#         response = requests.get(url, headers=self.headers, verify=False)
#         response.raise_for_status()
#         return response.json()
    

import requests
import json
import urllib3
import logging
from prometheus_client import Gauge, generate_latest, REGISTRY

# # Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# # Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# # Constants
PROM_NAMESPACE = "pbs"
VERSION_API = "/api2/json/version"
DATASTORE_USAGE_API = "/api2/json/status/datastore-usage"
DATASTORE_API = "/api2/json/admin/datastore"
NODE_API = "/api2/json/nodes"
NODE_API_STATUS = "/api2/json/nodes/localhost/status"
TASKS_API = "/api2/json/nodes/localhost/tasks"

# Clear previous metrics
for metric in REGISTRY.collect():
    if metric.name.startswith(PROM_NAMESPACE):
        REGISTRY.unregister(metric)

# Define Prometheus Gauges
task_gauge = Gauge(f'{PROM_NAMESPACE}_task_status', 'Proxmox Backup Server task status',
                    ['upid', 'node', 'pid', 'worker_type', 'user', 'worker_id', 'status'])
cpu_gauge = Gauge(f'{PROM_NAMESPACE}_node_cpu', 'CPU usage of the node', ['node'])
memory_total_gauge = Gauge(f'{PROM_NAMESPACE}_node_memory_total', 'Total memory of the node', ['node'])
memory_used_gauge = Gauge(f'{PROM_NAMESPACE}_node_memory_used', 'Used memory of the node', ['node'])
memory_free_gauge = Gauge(f'{PROM_NAMESPACE}_node_memory_free', 'Free memory of the node', ['node'])
swap_total_gauge = Gauge(f'{PROM_NAMESPACE}_node_swap_total', 'Total swap of the node', ['node'])
swap_used_gauge = Gauge(f'{PROM_NAMESPACE}_node_swap_used', 'Used swap of the node', ['node'])
swap_free_gauge = Gauge(f'{PROM_NAMESPACE}_node_swap_free', 'Free swap of the node', ['node'])
uptime_gauge = Gauge(f'{PROM_NAMESPACE}_node_uptime', 'Uptime of the node', ['node'])
loadavg1_gauge = Gauge(f'{PROM_NAMESPACE}_node_loadavg_1', '1-minute load average of the node', ['node'])
loadavg5_gauge = Gauge(f'{PROM_NAMESPACE}_node_loadavg_5', '5-minute load average of the node', ['node'])
loadavg15_gauge = Gauge(f'{PROM_NAMESPACE}_node_loadavg_15', '15-minute load average of the node', ['node'])

class PBSClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {'Authorization': f'PBSAPIToken={token}'}

    def get(self, endpoint):
        url = f'{self.base_url}{endpoint}'
        logger.debug(f"Requesting URL: {url}")
        response = requests.get(url, headers=self.headers, verify=False)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.content}")
        response.raise_for_status()
        try:
            data = response.json()
            logger.debug(f"JSON response: {data}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {e}")
            return {}

    def get_version(self):
        return self.get(VERSION_API)

    def get_status(self):
        return self.get(DATASTORE_USAGE_API)
    
    def get_datastore_usage(self):
        return self.get(DATASTORE_USAGE_API)

    def get_datastores(self):
        return self.get(DATASTORE_API)

    def get_nodes(self):
        return self.get(NODE_API)
    
    def get_tasks(self):
        return self.get(TASKS_API)
    
    def get_nodes_status(self):
        return self.get(NODE_API_STATUS)

    def collect_metrics(self):
        tasks = []  # self.get_tasks().get('data', [])
        

        for task in tasks:
            labels = {
                'upid': task['upid'],
                'node': task['node'],
                'pid': str(task['pid']),
                'worker_type': task['worker_type'],
                'user': task['user'],
                'worker_id': task.get('worker_id', ''),
                'status': task.get('status', ''),
            }
            task_gauge.labels(**labels).set(1)

        
        # Clear previous metrics
        # for metric in REGISTRY.collect():
        #     if metric.name.startswith(PROM_NAMESPACE):
        #         REGISTRY.unregister(metric)

        # Define Prometheus Gauges
        node_status = self.get_nodes_status().get('data', {})
        logger.debug("get_nodes_status......................")
        labels = {
            'node': 'localhost',
        }
        # Define Prometheus Gauges for node status
        # cpu_gauge = Gauge(f'{PROM_NAMESPACE}_node_cpu', 'CPU usage of the node', ['node'])
        # memory_total_gauge = Gauge(f'{PROM_NAMESPACE}_node_memory_total', 'Total memory of the node', ['node'])
        # memory_used_gauge = Gauge(f'{PROM_NAMESPACE}_node_memory_used', 'Used memory of the node', ['node'])
        # memory_free_gauge = Gauge(f'{PROM_NAMESPACE}_node_memory_free', 'Free memory of the node', ['node'])
        # swap_total_gauge = Gauge(f'{PROM_NAMESPACE}_node_swap_total', 'Total swap of the node', ['node'])
        # swap_used_gauge = Gauge(f'{PROM_NAMESPACE}_node_swap_used', 'Used swap of the node', ['node'])
        # swap_free_gauge = Gauge(f'{PROM_NAMESPACE}_node_swap_free', 'Free swap of the node', ['node'])
        # uptime_gauge = Gauge(f'{PROM_NAMESPACE}_node_uptime', 'Uptime of the node', ['node'])
        # loadavg1_gauge = Gauge(f'{PROM_NAMESPACE}_node_loadavg_1', '1-minute load average of the node', ['node'])
        # loadavg5_gauge = Gauge(f'{PROM_NAMESPACE}_node_loadavg_5', '5-minute load average of the node', ['node'])
        # loadavg15_gauge = Gauge(f'{PROM_NAMESPACE}_node_loadavg_15', '15-minute load average of the node', ['node'])

        # Set values for Prometheus Gauges
        cpu_gauge.labels(node='localhost').set(node_status.get('cpu', 0))
        memory_total_gauge.labels(node='localhost').set(node_status.get('memory', {}).get('total', 0))
        memory_used_gauge.labels(node='localhost').set(node_status.get('memory', {}).get('used', 0))
        memory_free_gauge.labels(node='localhost').set(node_status.get('memory', {}).get('free', 0))
        swap_total_gauge.labels(node='localhost').set(node_status.get('swap', {}).get('total', 0))
        swap_used_gauge.labels(node='localhost').set(node_status.get('swap', {}).get('used', 0))
        swap_free_gauge.labels(node='localhost').set(node_status.get('swap', {}).get('free', 0))
        uptime_gauge.labels(node='localhost').set(node_status.get('uptime', 0))
        loadavg1_gauge.labels(node='localhost').set(node_status.get('loadavg', [0, 0, 0])[0])
        loadavg5_gauge.labels(node='localhost').set(node_status.get('loadavg', [0, 0, 0])[1])
        loadavg15_gauge.labels(node='localhost').set(node_status.get('loadavg', [0, 0, 0])[2])
