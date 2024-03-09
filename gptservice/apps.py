import json
import os
import boto3
import sys
from openai import OpenAI
from .Tools.services import SERVICES
from .Tools.features.aws_services import AWS
from .Tools.features.google_shopping import GoogleShopping
from .Tools.features.google_flights import GoogleFlights

AWS_SECRET_ACCESS_KEY=os.environ.get('aws_secret_key')
AWS_ACCESS_KEY_ID=os.environ.get('aws_access_key')
API_KEY=os.environ.get('openai_key')
GPT_MODEL = "gpt-3.5-turbo-0613"
tools = [
    SERVICES['AWS'].tools,SERVICES['GoogleShopping'].tools,SERVICES['GoogleFlights'].tools
        
]  
client = OpenAI(api_key=API_KEY)


def call_assistant(userPrompt,tools=tools):
    chat_response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "system", "content": "Hello, I'm an AI assistant created by OpenAI. Sukamal has developed this API service, which offers several functionalities. These include provisioning AWS services such as EC2 and S3. Additionally, there are features like a Shopping Assistant and a Flight Booking Assistant. The Flight Booking Assistant is capable of extracting airport codes (IDs) from user input. Let's discuss the functionalities in more detail."},
                  {"role": "user", "content": userPrompt}
                  ],
        functions=tools,
        function_call='auto'
    )
    try:  
        assistant_message = json.loads(chat_response.choices[0].message.function_call.arguments)
        print("Keywords: %s"% assistant_message)
        if not all((assistant_message)):
            assistant_message = chat_response.choices[0].message.content
            return assistant_message
        else:
             message = process_service(assistant_message, userPrompt)
             return message


    except Exception as e:
        assistant_message = chat_response.choices[0].message.content
        return assistant_message

def process_service(assistant_message, userPrompt):
                SERVICES_CONFIG = {
                    'AWS': ['service_name', 'operation', 'region', 'name'],
                    'GoogleShopping': ['item', 'brand', 'price'],
                    'GoogleFlights': ['arrival_id', 'departure_id', 'outbound_date', 'return_date'],
        # Add more services and their parameters as needed
                }
                # Extract service and params from assistant message
                service, *required_params = extract_payload(assistant_message)
                if not all(required_params):
                    content = SERVICES.get(service).content
                    assistant_message = natural_language_processing(userPrompt, content)
                    return assistant_message
                
                elif all(required_params):
                    payload_params = SERVICES_CONFIG[service]
                    payload = {param: value for param, value in zip(payload_params, required_params)}
                    service_class = getattr(sys.modules[__name__], service, None)

                    # Check if the service class exists
                    if service_class is not None:
                    # If it exists, instantiate it with the payload
                        trigger = service_class(**payload)
                        results = trigger.invoke_service()
                        content = SERVICES.get(service).content
                        assistant_response = natural_language_processing(results, content)
                        return assistant_response
                    else:
                    # If it doesn't exist, raise an error or handle it appropriately
                        raise ValueError(f'Invalid service name: {service}')

                    

def extract_payload(assistant_message):
    try:
        service_mapping = {
            'service_name': 'AWS',
            'item': 'GoogleShopping',
            'arrival_id': 'GoogleFlights'
        }
        payload_mapping = {
            'AWS': ['service_name', 'operation', 'region', 'name'],
            'GoogleShopping': ['item', 'brand', 'price'],
            'GoogleFlights': ['arrival_id', 'departure_id', 'outbound_date', 'return_date']         
        }

        service = None
        params = []
        for key, value in assistant_message.items():
            if key in service_mapping:
                service = service_mapping[key]
                payload = payload_mapping[service]
                params = [assistant_message.get(param).lower() if param == 'service_name' else 'gpt-test' if param == 'name' and assistant_message.get('name') is None else assistant_message.get(param) for param in payload]
                break      
        if service is not None:
            return [service] + params
        else:
            return
        
    except Exception as e:
        print(e)
        return


def natural_language_processing(results,content):
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "system", "content": content},
                  {"role": "user", "content": json.dumps(results)}]
    )
    return response.choices[0].message.content

def main(): 
       
    while True:
        userPrompt = input("Enter your prompt ('q' to quit): ")
        if userPrompt.lower() == 'q':
            break
        api_out = call_assistant(userPrompt, tools)
        print(api_out)
        # assistant_response = natural_language_processing(api_out)
        # print(assistant_response)
if __name__ == "__main__":
     main()
    





