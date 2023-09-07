# LDN-Scraper

This repository scrapes data daily from https://www.lagrangenews.com and sends an email of all the articles of a given date. When configured with AWS Lambda and EventBridge, this code can be executed 
daily. To run the code, follow the steps below:
1. Install all dependencies with `pip install -r requirements.txt`.
2. Set up environment variables of access_key, secret_access_key, and email.
3. Create a topic in AWS SNS called "LDN" and an S3 bucket called "ldnscraper".
4. Configure AWS Lambda to execute the lambda_handler function in AWSHandler.py. Be sure to upload all required dependencies to execute the code.
5. Set up AWS EventBridge to execute the lambda function configured above once daily (end of day is recommended since articles may be written in the middle of the day).

Sample Email:
<img width="1638" alt="Screenshot 2023-09-07 at 10 42 22 AM" src="https://github.com/neilhpatel/LDN-Scraper/assets/69949115/7fccdd61-0ccc-4ec6-82de-2d32233471c4">
