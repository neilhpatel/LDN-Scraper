import os
from datetime import date
import boto3
import json
import time

from NewsScraper import NewsScraper

"""
AWSHandler interacts with AWS services (sending email, pushing to S3, Lambda function)
"""
class AWSHandler:

    def __init__(self):
        self.aws_access_key_id = os.getenv('access_key')
        self.aws_secret_access_key = os.getenv('secret_access_key')
        self.email = os.getenv('email')

        self.sns = boto3.client(
            'sns',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name='us-east-1'
        )

        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name='us-east-1'
        )

    """
    Retrive the topic ARN to send an email to
    """
    def retriveTopicARN(self):
        response = self.sns.list_topics()
        if 'Topics' in response:
            for topic in response['Topics']:
                topic_arn = topic['TopicArn']
                if "LDN" in topic_arn:
                    return topic_arn

        else:
            raise Exception("No SNS topic for LDN found")

    """
    Sends an email to the topic ARN containing the email subject and the message (text of articles)
    """
    def send_email(self, subject, message):
        topic_arn = self.retriveTopicARN()

        response = self.sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
        print(f"Successfully sent email to all subscribers of LDN topic")

    """
    Writes text to a txt file
    """
    def writeToTxtFile(self, fileName, articles):
        with open(fileName, 'w') as file:
            file.write(articles)

        print(f"Articles have been written to '{fileName}'.")

    """
    Pushes txt file to an S3 bucket
    """
    def pushToS3(self, articles):
        bucketName = 'ldnscraper'
        fileName = date.today().strftime("%B %d, %Y") + '.txt'


        try:
            self.s3.put_object(Bucket=bucketName, Key=fileName, Body=articles)
            print(f'Successfully uploaded {fileName} to {bucketName}')
        except Exception as e:
            print(f'Error uploading {fileName} to {bucketName}: {e}')


"""
Function executed by AWS Lambda. Configured in EventBridge to run once daily 
"""

def lambda_handler(event, context):
    vLocalTimeZone = 'US/Eastern'
    os.environ['TZ'] = vLocalTimeZone #Change default time zone of AWS Lambda to EST
    time.tzset()
    todaysDate = time.strftime('%Y/%m/%d')
    print(f"Getting articles from {todaysDate}")
    scraper = NewsScraper(todaysDate)
    articles = scraper.readHomePage()

    ldn = LDNNewsletter()

    subject = "Lagrange Daily News Articles From " + todaysDate
    if articles is None or len(articles) == 0:
        articles = "No new articles for " + todaysDate
    ldn.pushToS3(articles)
    ldn.send_email(subject, articles)

    return {
        'statusCode': 200,
        'body': json.dumps('Request Succeeded.')
    }