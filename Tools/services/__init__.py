from Tools.services.aws_ec2 import ec2

SERVICES = {
    ec2().service: ec2()
}