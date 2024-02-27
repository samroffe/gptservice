import boto3
import os
import json
from botocore.exceptions import ClientError
AWS_SECRET_ACCESS_KEY=os.environ.get('aws_secret_key')
AWS_ACCESS_KEY_ID=os.environ.get('aws_access_key')




class AWS:
    def __init__(self, service_name, region_name, server_name="gpt-test", operation=None):
        self.service_name = service_name
        self.region_name = region_name
        self.server_name = server_name
        self.operation = operation

    def invoke_service(self):   
        try:
            if self.service_name and self.region_name is not None:
                print('------- Request for External AWS API ----------')
                service_function = {
                    "ec2": 'manage_ec2',
                    "amazonec2": 'manage_ec2',
                    "s3": 'manage_s3',
                    "amazon ec2": 'manage_ec2'
                }
                service_found = False
                for service, function_name in service_function.items():
                     if any(keyword.lower() in self.service_name.lower() for keyword in service.split()):
                            service_found = True
                            self.service_name = service
                            session = boto3.resource(
                                self.service_name,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                region_name=self.region_name
                        )
                            getattr(self, service_function[self.service_name])(self.server_name, session, self.region_name, self.operation)
                            break

            else:
                print('Service variables are not set. Please check the service name and region name.')
                return
    
        except Exception as e:
            print('Error running AWS api request')
            print(e)

    def manage_ec2(self, server_name, ec2, region_name, operation=None):
        api_result = {}
        #action = "create_instances" if any(word.lower() in operation.lower() for word in ["build","create","deploy","make","construct","generate","produce","design"]) else "terminate_instances"
        try:
            api_result = ec2.create_instances(
                ImageId="ami-0e670eb768a5fc3d4",
                InstanceType="t2.micro",
                KeyName="apikey", 
                MinCount=1,
                MaxCount=1
            )[0]
            api_result.wait_until_running()
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
            # print(api_result)
            instance = ec2.Instance(api_result.id)
            instance_details = {
                "id": instance.id,
                "Type": instance.instance_type,
                "State": instance.state['Name'],
                "Public IP": instance.public_ip_address,
            }
            print(instance_details)

            # return api_result
        except ClientError as e:
            print(e)

    def manage_s3(self, server_name, s3, region_name, operation=None):
        api_result = {}
        api_result = s3.create_bucket(Bucket=server_name,
                                    ACL='private',
                                    CreateBucketConfiguration={
                                        'LocationConstraint': region_name
                                    })
        api_result.wait_until_exists()
        api_result.load()

        print(api_result) 