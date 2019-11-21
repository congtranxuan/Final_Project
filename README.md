# Final Project: Computer Vision, Facial Rekognition

## Introduction:

The focus of this project demonstrates just one of the ways computer vision can be use, specifically for this project we demonstrate the use of AWS-Amazon Rekognition to detect facial expressions and even recognize individuals with a high degree of accuracy. 

Computer vision is a growing innovative industry and one that has been used from recognizing objects during the manufacturing process for quality control, security recognition, and even highly accurate surgical procedures.   

Our project can be found in the link below:
https://PROVIDE-CORRECT-LINK-HERE-.herokuapp.com

![](Images/ CORRECT IMAGE HERE .png)

## Data Source: Computer Vision: The Story using Tableau
Information on companies using Machine Vision (software) was collected from ThomasNet.com (https://www.thomasnet.com/products/machine-vision-software-45328275-1.html). A total of 68 companies are presented which include location, services provided and their respective industries, number of employees for each company, and specific use of machine vision software (specific uses not presented in Tableau visualizations). These data are presented in map format on Tableau and through the Tableau tooltip.  

Data collected was entered into a csv file and read into Tableau. Office locations represent city and not actual office locations. A second file was downloaded and merged for latitude and longitude data for city locations from Simple Maps found at https://simplemaps.com/data/us-zips.




## Getting Started:

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system.

### Prerequisites for AWS Configuration
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

Additionally, the following libraries are required


Tools required:
1.	D3
2.	SQLAlchemy
3.	SQLite
4.	Bootstrap
5.	Jinja
6.	HTML
7.	Javascript
8.	CSS
9.	Amazon Web Services (AWS)
10.	S3
11.	Amazon Rekognition
12.	Flask

Platform used to to serve website:


13.	Heroku

### Installing

* install python libraries
* install anaconda v.3.7
* install javascript libraries (D3, jQuery)
* install Flask
* install SQLAlchemy


## Running the tests

1. Use Visual Studio Code to load the project folders.
2. Open file index.html and app.py in VS Code.
3. Run the code in VSC using app.py (shortcut key function F5) - which will take you to - http://127.0.0.1:5000/ to view the html template.
![](Images/ CORRECT IMAGE HERE .jpg)
Last but not least, download "https://github.com/congtranxuan/Final_Project" to a local directory.
1.  folder contains:
   - static folder contains [css, db(contains clean data files), images, js, php, webfonts, privacy policy, terms conditions]
   - templates contains (index.html)


![](Images/ CORRECT IMAGE FILE HERE .jpg)

## Built With

* [D3] (https://d3js.org) - Used for creating a chart
* [HTML]  - used to create the web template
* [Heroku] (https://www.heroku.com) - used to deploy to online server

![](Images/ CORRECT IMAGE HERE .png)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

v 1.0

## Authors

* Xuan Cong Tran
* Nithya Iyengar
* Will Copeland
* Misael Obregon

## License

This project is licensed under the Rice License - see the [LICENSE.md](LICENSE.md) file for details
