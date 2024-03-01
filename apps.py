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
                service_name, operation, region, name = extract_payload(assistant_message)
                item, brand, amount, price = extract_payload(assistant_message)
                if not service_name or not region:
                    content = SERVICES['aws'].content
                    assistant_message = natural_language_processing(userPrompt, content)
                    return assistant_message
                
                elif service_name and region and operation:
                    aws = AWS(service_name, region, name, operation)
                    results = aws.invoke_service()
                    content = SERVICES['aws'].content
                    assistant_response = natural_language_processing(results, content)
                    return assistant_response
                
                elif not item or not brand or not price:
                    content = SERVICES['shopping'].content
                    assistant_message = natural_language_processing(userPrompt, content)
                    return assistant_message
                
                elif item and brand and price:
                    pass

def extract_payload(assistant_message):
    try:
        # assistant_message = json.loads(chat_response.choices[0].message.function_call.arguments)
        # print(assistant_message)
        if 'service_name' in assistant_message:
            service_name = assistant_message.get('service_name').lower()
            operation = assistant_message.get('operation', 'build')
            region = assistant_message.get('region', '')
            name = assistant_message.get('name', 'gpt-test')
            return service_name, operation, region, name
                
        elif 'item' in assistant_message:
            item = assistant_message['item']
            amount = assistant_message['amount']
            brand = assistant_message['brand']
            price = assistant_message['price']
            return item, brand, amount, price
    except Exception as e:
        print(e)

def extractShoppingDetail(item, brand, price, amount=1):
    print(f'Item: {item}, Amount: {amount}, Brand: {brand}, Price: {price}')


def natural_language_processing(results,content):
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "system", "content": content},
                  {"role": "user", "content": json.dumps(results)}]
    )
    return response.choices[0].message.content

def main():
    tools = [
    SERVICES['shopping'].tools, SERVICES['aws'].tools
        
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
    





