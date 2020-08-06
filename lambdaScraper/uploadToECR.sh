ACCOUNT_NUMBER='714521125543'
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ACCOUNT_NUMBER.dkr.ecr.us-east-1.amazonaws.com
docker build -t factset-scraper .
docker tag factset-scraper:latest $ACCOUNT_NUMBER.dkr.ecr.us-east-1.amazonaws.com/factset-scraper:latest
docker push $ACCOUNT_NUMBER.dkr.ecr.us-east-1.amazonaws.com/factset-scraper:latest
