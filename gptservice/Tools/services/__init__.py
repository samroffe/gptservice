from .aws_svc import aws
from .shopping import shopping
from .flights import flights
from .bookmyshow import bookmyshow

SERVICES = {
    aws().service: aws(),
    shopping().service: shopping(),
    flights().service: flights(),
    bookmyshow().service: bookmyshow()

    
}

