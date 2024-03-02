import json
import os
import boto3
import sys
from openai import OpenAI
from Tools.services import SERVICES
from Tools.features.aws_services import AWS
from Tools.features.google_shopping import GoogleShopping

AWS_SECRET_ACCESS_KEY=os.environ.get('aws_secret_key')
AWS_ACCESS_KEY_ID=os.environ.get('aws_access_key')
API_KEY=os.environ.get('openai_key')
GPT_MODEL = "gpt-3.5-turbo-0613"

client = OpenAI(api_key=API_KEY)


def call_assistant(tools, userPrompt):
    chat_response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": userPrompt}],
        functions=tools,
        function_call='auto'
    )
    try:  
        assistant_message = json.loads(chat_response.choices[0].message.function_call.arguments)
        if not all((assistant_message)):
            assistant_message = chat_response.choices[0].message.content
            return assistant_message
        else:
             message = process_service(assistant_message, userPrompt)
             return message
            # item,amount,brand,price = extract_payload(chat_response)
            # extractShoppingDetail(item, brand, price, amount)
            # assistant_input = invoke_aws(service_name, region_name, server_name, operation)
            # return assistant_input

    except Exception as e:
        assistant_message = chat_response.choices[0].message.content
        return assistant_message

def process_service(assistant_message, userPrompt):
                SERVICES_CONFIG = {
                    'AWS': ['service_name', 'operation', 'region', 'name'],
                    'GoogleShopping': ['item', 'brand', 'price', 'amount']
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
                    print(payload)
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
        # assistant_message = json.loads(chat_response.choices[0].message.function_call.arguments)
        # print(assistant_message)
        if 'service_name' in assistant_message:
            service = 'AWS'
            service_name = assistant_message.get('service_name').lower()
            operation = assistant_message.get('operation', 'build')
            region = assistant_message.get('region', '')
            name = assistant_message.get('name', 'gpt-test')
            return service, service_name, operation, region, name
                
        elif 'item' in assistant_message:
            service = 'GoogleShopping'
            item = assistant_message.get('item','')
            amount = assistant_message.get('amount', 1)
            brand = assistant_message.get('brand','')
            price = assistant_message.get('price','')
            return service, item, brand, amount, price
        
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
    tools = [
    SERVICES['AWS'].tools,SERVICES['GoogleShopping'].tools
        
]   
       
    while True:
        userPrompt = input("Enter your prompt ('q' to quit): ")
        if userPrompt.lower() == 'q':
            break
        api_out = call_assistant(tools, userPrompt)
        print(api_out)
        # assistant_response = natural_language_processing(api_out)
        # print(assistant_response)
if __name__ == "__main__":
     main()
    





