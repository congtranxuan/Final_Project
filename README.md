# Final_Project

# AWS Configuration
Required configuration for AWS Rekognition access are:
pip install boto3
pip install awscli

aws config
https://docs.aws.amazon.com/rekognition/latest/dg/setup-awscli-sdk.html
For AWS configuration following details will be required.
- Create an account with Identity and Access Management(IAM)
-Using Users tab add user name. This will generate the Access Key ID and Secret Key to be input in aws config.
-Select a state/timezone - the http link will contain the zone number.
Add Groups (AWSrekognition)
Add permissions: 
- AmazonRekognitionReadOnlyAccess
- AmazonRekognitionFullAccess
- AmazonRekognitionServiceRole
Use S3 to create buckets
-Uncheck Block off public access



# Tableau Story and Dashboard
Information on companies using Machine Vision (software) was collected from ThomasNet.com (https://www.thomasnet.com/products/machine-vision-software-45328275-1.html). Information on a total of 68 companies are presented which include location, services provided and associated industries, number of employees and specific use of machine vision software (specific uses not presented in Tableau visualizations). Data collected was entered into a csv file and read into Tableau.

Office locations represent city and not actual office locations. A second file was downloaded and merged for latitude and longitude data for city locations from Simple Maps found at https://simplemaps.com/data/us-zips.

Data presented on Tableau shows company locations, size of company (per number of employees), tooltip, and services provided (represented in clusters).  

