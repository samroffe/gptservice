import json
import os
import boto3
from openai import OpenAI
from Tools.services import SERVICES

AWS_SECRET_ACCESS_KEY=os.environ.get('aws_secret_key')
AWS_ACCESS_KEY_ID=os.environ.get('aws_access_key')
API_KEY=os.environ.get('openai_key')
GPT_MODEL = "gpt-3.5-turbo-0613"

client = OpenAI(api_key=API_KEY)


def call_assistant(tools, userPrompt):
    chat_response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": userPrompt}],
        tools=tools,
        tool_choice="auto"
    )
    try:
        assistant_message = json.loads(chat_response.choices[0].message.tool_calls[0].function.arguments)
        print(assistant_message)
        service_name = assistant_message['service_name'].lower()
        operation = assistant_message['operation']
        region_name = assistant_message['region']
        server_name = assistant_message['name']
        invoke_aws(service_name, region_name, server_name, operation)
        # assistant_input = invoke_aws(service_name, region_name, server_name, operation)
        # return assistant_input


    except Exception as e:
        assistant_message = chat_response.choices[0].message.content
        print(assistant_message)


def invoke_aws(service_name, region_name, server_name, operation):   
    try:
        if service_name and region_name is not None:
            print('------- Request for External AWS API ----------')
            service_function = {
                "ec2": manage_ec2,
                "amazoneec2": manage_ec2,
                "s3": manage_s3,
            }
            if service_name in service_function:
                session = boto3.resource(
                    service_name,
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=region_name
                )
                service_function[service_name](server_name, operation, region_name, session) 
           
            else:
                print('Service not available')
                return
    
    except Exception as e:
        print('Error running AWS api request')
        print(e)

def manage_ec2(server_name, operation, region_name, ec2):
    api_result = {}
    action = "create_instances" if any(word in operation.lower() for word in ["runInstances", "TerminateInstances"]) else "terminate_instances"
    api_result = ec2.create_instances(
            ImageId="ami-0e670eb768a5fc3d4",
            InstanceType="t2.micro",
            KeyName="apikey", 
            MinCount=1,
            MaxCount=1
        )[0]
    api_result.wait_until_running()
    if action == "create_instances":
        api_result.create_tags(
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': server_name
                        },
        # Add any additional tags here if needed
    ]
)
    api_result.load()
    print(api_result)
    # return api_result

def manage_s3(server_name, operation, s3):
    pass




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
    SERVICES['ec2'].tools
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
    





