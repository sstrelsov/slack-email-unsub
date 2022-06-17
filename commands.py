import os

api_key = {'Api_Key': str(os.environ.get('ITERABLE_API_KEY'))}

def api_url(endpoint):
    return f'https://api.iterable.com/api{endpoint}'

def request_body(endpoint):
    return f'https://api.iterable.com/api{endpoint},headers={api_key}'
