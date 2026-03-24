import os


bind = "0.0.0.0:8000"
workers = int(os.getenv("GUNICORN_WORKERS", "2"))
threads = int(os.getenv("GUNICORN_THREADS", "2"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "120"))

accesslog = "-"
errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "debug")
capture_output = True
enable_stdio_inheritance = True

access_log_format = (
    '%(h)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" '
    "rt=%(M)sms req_id=%({x-request-id}i)s fwd=%({x-forwarded-for}i)s"
)
