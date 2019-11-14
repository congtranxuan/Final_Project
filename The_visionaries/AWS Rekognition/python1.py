import boto3
import pprint
import json

client=boto3.client('rekognition')
response = client.compare_faces(
    SimilarityThreshold=90,
    SourceImage={
        'S3Object': {
            'Bucket': 'finalprojectawsrekognition',
            'Name': 'jessica2.jpg',
        },
    },
    TargetImage={
        'S3Object': {
            'Bucket': 'finalprojectawsrekognition',
            'Name': 'jessica1.jpeg',
        },
    },
)

print(json.dumps(response))