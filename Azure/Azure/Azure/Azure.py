import requests
import datetime
from flask import Flask

app = Flask(__name__)

tenant_id = 'bee53ca7-4878-4548-90d6-ef673a0d7271'
client_id = 'f21cd79c-2839-4e77-9ea8-097f3e308d5a'
client_secret = 'a9c7ce98-25d8-4536-8dfa-4390b1a1ef0d'  # Reemplaza con tu Client Secret
subscription_id = '7577655b-4420-4a12-a431-712303899b92'  # Reemplaza con tu Subscription ID
resource_group = 'Alex384'  # Reemplaza con tu Resource Group
resource_name = 'PreguntasyRespuestas'  # Reemplaza con tu Resource Name

def get_token():
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://monitoring.azure.com/.default'
    }
    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()
    return response.json()['access_token']

def send_metrics(token):
    resource_id = f'/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Insights/metrics'
    url = f'https://management.azure.com{resource_id}?api-version=2018-01-01'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    metric_data = {
        "timeseries": [
            {
                "data": [
                    {
                        "timeStamp": datetime.datetime.utcnow().isoformat(),
                        "total": 1
                    }
                ],
                "metrickind": "Custom",
                "name": {
                    "value": "customMetric",
                    "unit": "None"
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=metric_data)
    if response.status_code == 200:
        print('Metric sent to Azure Monitor:', response.json())
    else:
        print('Error sending metric:', response.status_code, response.text)

@app.before_request
def before_request():
    try:
        token = get_token()
        send_metrics(token)
    except Exception as e:
        print('Error in before_request:', e)

@app.route('/')
def index():
    return 'Se ha conectado a la Base de datos Azure'

if __name__ == '__main__':
    app.run(port=3000)
