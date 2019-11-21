import boto3

BUCKET = "finalprojectawsrekognition"
KEY_SOURCE = "jessica1.jpeg"
KEY_TARGET = "jessica2.jpg"

def compare_faces(bucket, key, bucket_target, key_target, threshold=80):
	rekognition = boto3.client("rekognition")
	response = rekognition.compare_faces(
	    SourceImage={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		TargetImage={
			"S3Object": {
				"Bucket": bucket_target,
				"Name": key_target,
			}
		},
	    SimilarityThreshold=threshold,
	)
	return response['SourceImageFace'], response['FaceMatches']


source_face, matches = compare_faces(BUCKET, KEY_SOURCE, BUCKET, KEY_TARGET)

# one match for each target face
for match in matches:
	print(match['Face']['Confidence'])
