#!/bin/bash
[[ -z "${downloadfolder}" ]] && downloadfolder="/" || downloadfolder="${downloadfolder}"
echo $downloadfolder
[[ -z "${count}" ]] && NO_OF_TASKS=3 || NO_OF_TASKS="${count}"
echo $NO_OF_TASKS
export LANG=C.UTF-8
for (( i=1; i<=$NO_OF_TASKS; i++ ))
do
	curl -k -X POST 'https://api.aic-identity-ssvc.factset.com/creds' \
	-H 'Content-Type:application/json' \
	-d '{
		"username": "svc-aws-435092708000@factset.com",
			"accountId": "435092708000",
			"roleName": "remote-execution-iam-role",
			"password": "SvC1g5TPWPIw8S_oIhse",
		"duration": 3600
	}'> cred.json
	echo "here r the creditionals"
	AWS_ACCESS_KEY_ID=$(jq -r '.awsAccessKey' cred.json)
	export AWS_ACCESS_KEY_ID
	AWS_SECRET_ACCESS_KEY=$(jq -r '.awsSecretKey' cred.json)
	export AWS_SECRET_ACCESS_KEY
	AWS_SESSION_TOKEN=$(jq -r '.awsSessionToken' cred.json)
	export AWS_SESSION_TOKEN
	echo $AWS_ACCESS_KEY_ID
	echo $AWS_SECRET_ACCESS_KEY
	echo $AWS_SESSION_TOKEN
	curl -X POST 'https://vpce-0537ee56e949aebdc-t0zmnz94.execute-api.us-east-1.vpce.amazonaws.com/test/smartspy' \
	-H 'x-apigw-api-id:e2gtsz1nv4' \
	> url.json
	cat url.json
	URLS=$(jq -r '.url' url.json)
	export URLS
	echo $URLS
	allowed_domains=$(jq -r '.allowed_domain' url.json)
	export allowed_domains
	echo $allowed_domains	
	scrapy crawl smartspyder -a start_urls=$URLS -a allowed_domains=$allowed_domains -a textextract=1 --logfile abc.txt &
	python3 S3push.py
done 

