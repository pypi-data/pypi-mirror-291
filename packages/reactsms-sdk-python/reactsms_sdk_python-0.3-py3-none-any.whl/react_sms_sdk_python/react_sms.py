# React SMS
# Copyright (c) 2022-2024 React SMS
# Licensed under the MIT License. See LICENSE file for more details.


import requests, base64, json


class ReactSMS():

    BASE_URL = "https://react-sms.com/messages"


    def __init__(self, auth_key:str, api_key:str, service_key:str=None):
        self.auth_key = auth_key
        self.api_key  = api_key
        self.service_key = service_key

        TOKEN = self.tokenBuilder()

        self.headers = {
            'Authorization': 'Bearer {}'.format(TOKEN),
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }


    def tokenBuilder(self):
        text = "{}:{}".format(self.auth_key, self.api_key)
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')



    def send(self, message:str, recipients:list):
        payload = {
            "message": message,
            "numbers": json.dumps(recipients),
            "serviceKey": self.service_key
        }

        try:
            response = requests.post(ReactSMS.BASE_URL+"/send", json=payload, headers=self.headers)
            response.raise_for_status() 
            data = response.json()

        except requests.exceptions.HTTPError as http_err:
            raise Exception({'error': str(http_err)})
            #JsonResponse({'error': str(http_err)}, status=400)

        except Exception as err:
            raise Exception({'error': str(err)})

        return data


    
    def balance(self):

        try:
            response = requests.get(ReactSMS.BASE_URL+"/get_balance", headers=self.headers)
            response.raise_for_status() 
            data = response.json()

        except requests.exceptions.HTTPError as http_err:
            raise Exception({'error': str(http_err)})
            #JsonResponse({'error': str(http_err)}, status=400)

        except Exception as err:
            raise Exception({'error': str(err)})

        return data
    


    def create_service(self, service_name:str, quota_sms:int, active_quota:bool, description:str):
        payload = {
            "service_name": service_name,
            "quota_sms": quota_sms,
            "active_quota": active_quota,
            "description" : description
        }

        try:
            response = requests.post(ReactSMS.BASE_URL+"/create_service", data=payload, headers=self.headers)
            response.raise_for_status() 
            data = response.json()

        except requests.exceptions.HTTPError as http_err:
            raise Exception({'error': str(http_err)})
            #JsonResponse({'error': str(http_err)}, status=400)

        except Exception as err:
            raise Exception({'error': str(err)})

        return data