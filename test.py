import boto3 
import os

AWS_SECRET_ACCESS_KEY=os.environ.get('aws_secret_key')
AWS_ACCESS_KEY_ID=os.environ.get('aws_access_key')

ec2 = boto3.client('ec2', region_name='us-east-1', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
response = ec2.describe_images(
    Filters=[
        {
            'Name': 'architecture',
            'Values': ['x86_64']  # Optionally, filter by architecture
        },
        {
            'Name': 'state',
            'Values': ['available']  # Optionally, filter by state
        },
        {
            'Name': 'owner-alias',
            'Values': ['amazon']  # Optionally, filter by owner alias
        },
        {
            'Name': 'root-device-type',
            'Values': ['ebs']  # Optionally, filter by root device type
        },
        {
            'Name': 'virtualization-type',
            'Values': ['hvm']  # Filter by HVM virtualization type
        },
        {
            'Name': 'name',
            'Values': ['al2023-ami-2023.3.*']  # Filter by name containing "al2023"
        }
    ]
)

# Sort images by creation date
sorted_images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)

# Get the most recent image
most_recent_image = sorted_images[0]['ImageId'] if sorted_images else None

print(most_recent_image)
# # Print the details of the most recent image
# if most_recent_image:
#     print(f"Most Recent Image: ID - {most_recent_image['ImageId']}, Name - {most_recent_image['Name']}, Creation Date - {most_recent_image['CreationDate']}")
# else:
#     print("No available images found.")