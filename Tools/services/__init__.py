from Tools.services.aws_ec2 import ec2
from Tools.services.shopping import shopping

SERVICES = {
    ec2().service: ec2(),
    shopping().service: shopping()

}