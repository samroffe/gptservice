import json
import os
import boto3
from openai import OpenAI
from Tools.services import SERVICES
from Tools.features.aws_services import AWS

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
        service_name, operation, region, name = extract_payload(chat_response)
        aws=AWS(service_name, region, name, operation)
        aws.invoke_service()
        # item,amount,brand,price = extract_payload(chat_response)
        # extractShoppingDetail(item, brand, price, amount)
        # assistant_input = invoke_aws(service_name, region_name, server_name, operation)
        # return assistant_input

    except Exception as e:
        assistant_message = chat_response.choices[0].message.content
        print(assistant_message)

def extract_payload(chat_response):
    try:
         assistant_message = json.loads(chat_response.choices[0].message.function_call.arguments)
         print(assistant_message)
    except Exception as e:
        print(e)
        return  None
    if 'service_name' in assistant_message:
            service_name = assistant_message.get('service_name').lower()
            operation = assistant_message.get('operation', 'build')
            region = assistant_message.get('region', 'ap-south-1')
            name = assistant_message.get('name', 'gpt-test')
            return service_name, operation, region, name
                
    elif 's3' in assistant_message:
            item = assistant_message['item']
            amount = assistant_message['amount']
            brand = assistant_message['brand']
            price = assistant_message['price']
            return item, brand, amount, price  
    return None 


def extractShoppingDetail(item, brand, price, amount=1):
    print(f'Item: {item}, Amount: {amount}, Brand: {brand}, Price: {price}')


# def natural_language_processing(results):
#     response = client.chat.completions.create(
#         model=GPT_MODEL,
#         messages=[{"role": "system", "content": "You are a assistant. Provide the service details and get the id in natural language."},
#                   {"role": "system", "content": results}],
#         max_tokens=50
#     )
#     return response.choices[0].message.content

def main():
    tools = [
    SERVICES['shopping'].tools, SERVICES['ec2'].tools
        
]
    while True:
        userPrompt = input("Enter your prompt ('q' to quit): ")
        if userPrompt.lower() == 'q':
            break
        call_assistant(tools, userPrompt)
        # ai = natural_language_processing(final)
        # print(ai)
if __name__ == "__main__":
     main()
    





