from collections import namedtuple
from math import floor

Bucket = namedtuple('Bucket', ['number', 'start_lambda', 'stop_lambda'])
Data_bucket = namedtuple('Data_bucket', ['number', 'start_lambda', 'stop_lambda' 'data'])

def bucket(lambda_min, lambda_max, width):
    buckets = []
    bucket_num = 1
    total_buckets = int(floor(((lambda_max - lambda_min)/width)))
    print total_buckets
    while bucket_num < total_buckets:
        print bucket_num
        if bucket_num == 1:
            buckets.append(Bucket(bucket_num, lambda_min, (lambda_min+width)))
        else:
            buckets.append(Bucket(bucket_num, (lambda_min+(width*bucket_num)), lambda_min+(width*(bucket_num+1))))
        bucket_num += 1
    return buckets



