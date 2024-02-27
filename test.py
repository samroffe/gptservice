service_name = "amazon s3"
service_function = {
    "ec2": 'manage_ec2',
    "amazonec2": 'manage_ec2',
    "s3": 'manage_s3',
    "amazon ec2": 'manage_ec2'
}

service_found = False
for service, function_name in service_function.items():
    if any(keyword.lower() in service_name.lower() for keyword in service.split()):
        service_found = True
        print("Function to manage {} service: {}".format(service, function_name))
        break

if not service_found:
    print("Service not supported.")