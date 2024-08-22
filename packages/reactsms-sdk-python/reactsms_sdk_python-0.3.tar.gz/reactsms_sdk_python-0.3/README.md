# react-sms-sdk-python


React SMS SDK for Python 

With this SDK, you can:

- Send SMS

- Check your balance

- Create services


## Package Installation 


To install tihs package go to https://pypi.org/project/reactsms-sdk-python/ or run:

    pip install reactsms-sdk-python==0.2.1


## Package Usage 


    from react_sms_sdk_python.react_sms import ReactSMS


    class SMSAPI():

        AUTH_KEY = "rs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

        API_KEY = "rs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

        SERVICE_KEY = "xxxxxx"

        def __init__(self):
            self.sdk = ReactSMS(SMSAPI.AUTH_KEY, SMSAPI.API_KEY, SMSAPI.SERVICE_KEY)
        
        def send_message(self, message:str, phones:list):
            return self.sdk.send(message, phones)
        
        def balance(self):
            return self.sdk.balance()

        def create_service(self, service_name:str, quota_sms:int, active_quota:bool, description:str):
            return self.sdk.create_service(service_name, quota_sms, active_quota, description)