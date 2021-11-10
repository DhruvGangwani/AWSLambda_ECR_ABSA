## Aspect Based Sentiment Analysis

Aspect based sentiment analysis to compute the sentiment with respect to every aspect from tweets of twitter. AWS Lambda and ECR is used for production.

### Workflow
1. Scraps tweets from twitter with respect to a hashtag using Twitter Developer API.
2. Preprocess the tweet text to remove unwanted entities such as email, url, hashtag, mentions, emojis
3. Extracts nouns from the tweet
4. Find similarity between aspects and nouns to find alternative terms used to define aspects in that specific tweet
5. Using question answering model, get the phrases (adjectives and adverbs) which describes the aspect
6. Pass the phrases per aspect to sentiment analysis model to find the sentiment of the aspect.

### Production

Uses Docker image and pushes it to AWS ECR. Creating AWS lambda functionfrom the ECR image.

The purpose of creating lambda function using ECR is because the AWS lambda provides limit of 50MB zip  file and unzipped version should be upto 250MB  whereas ECR does not have such limits.

### Configure AWS
Use command 

```bash
aws configure
```
Enter AWS Access Key ID, AWS Secret Access Key, Region

### Configure ECR

1. Build Docker Image

```bash
docker build -t aspect_sentiment .   
```

2. Create Tag for image

```bash
docker tag  aspect_sentiment:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/aspect_sentiment.latest
```

3. Authenticate the Docker CLI to your Amazon ECR registry.

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com    

```
4. Create ECR Repository

```bash
aws ecr create-repository --repository-name aspect_sentiment --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

```

5. Push the image

```bash
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/aspect_sentiment:latest     
```

### Configure AWS Lambda
Create function and choose the image file from ECR


