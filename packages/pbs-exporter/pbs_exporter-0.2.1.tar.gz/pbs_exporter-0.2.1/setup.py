from setuptools import setup, find_packages

setup(
    name='pbs_exporter',
    version='0.2.1',
    description='Prometheus Exporter for Proxmox Backup Server',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'werkzeug',
        'prometheus_client',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'pbs_exporter=pbs_exporter.exporter:main'
        ]
    }
)
