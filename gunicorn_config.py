command = "/usr/local/bin/gunicorn"
pythonpath = '/home/ftp_root/reviews_bot_django/reviews'
bind = '127.0.0.1:8001'
workers = 3
user = 'ftp_root'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = ['DJANGO_SETTINGS_MODULE=reviews.settings']
