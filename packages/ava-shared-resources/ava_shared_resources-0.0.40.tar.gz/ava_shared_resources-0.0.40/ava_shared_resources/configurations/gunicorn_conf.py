"""The Configuration Module.

The module contains configuration for gunicorn start.
"""
from ava_shared_resources.configurations.gunicorn_config import GunicornConfigModel

cfg = GunicornConfigModel()

# http://docs.gunicorn.org/en/stable/settings.html#bind
bind = "{0}:{1}".format(cfg.gunicorn_host, cfg.gunicorn_port)

# http://docs.gunicorn.org/en/stable/settings.html#loglevel
loglevel = cfg.gunicorn_loglevel

# https://docs.gunicorn.org/en/stable/settings.html#logconfig
logconfig = cfg.gunicorn_logconfig

# https://docs.gunicorn.org/en/stable/settings.html#workers
workers = cfg.gunicorn_workers

# http://docs.gunicorn.org/en/stable/settings.html#worker-class
worker_class = cfg.gunicorn_worker_class

# http://docs.gunicorn.org/en/stable/settings.html#timeout
timeout = cfg.gunicorn_timeout

# https://docs.gunicorn.org/en/stable/settings.html#max-requests
max_requests = cfg.gunicorn_max_requests

# https://docs.gunicorn.org/en/stable/settings.html#max-requests-jitter
max_requests_jitter = cfg.gunicorn_max_requests_jitter

# https://docs.gunicorn.org/en/stable/settings.html#preload-app
preload_app = cfg.gunicorn_preload_app
