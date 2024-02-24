from Tools.services.features import Service


class ec2(Service):

    @property
    def service(self):
        return "ec2"
    
    @property
    def tools(self):
        return {
        "type": "function",
        "function": {
            "name": "invoke_aws_service",
            "description": "Invoke an AWS service",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "The name of the AWS service to invoke"
                    },
                    "operation": {
                        "type": "string",
                        "description": "Build or Terminate a service"
                    },
                    "region": {
                        "type": "string",
                        "description": "The AWS region to use for the service call"
                    },

                    "name": {
                        "type": "string",
                        "description": "The name of the instance"
                    }
                },
                "required": ["service_name", "operation", "region", "name"]
            }
        }
    }