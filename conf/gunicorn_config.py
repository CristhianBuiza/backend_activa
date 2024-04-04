command='/home/ubuntu/activa/venv/bin/gunicorn'
pythonpath = '/home/ubuntu/myproject'
bind = '172.31.35.3:8000'
workers = 3
accesslog = '/home/ubuntu/activa/logs/text/access.log'
errorlog = '/home/ubuntu/activa/logs/text/error.log'