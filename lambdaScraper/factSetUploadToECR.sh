ACCOUNT_NUMBER='450944449279'
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ACCOUNT_NUMBER.dkr.ecr.us-east-1.amazonaws.com
docker build -t scraper .
docker tag scraper:latest $ACCOUNT_NUMBER.dkr.ecr.us-east-1.amazonaws.com/scraper:latest
docker push $ACCOUNT_NUMBER.dkr.ecr.us-east-1.amazonaws.com/scraper:latest