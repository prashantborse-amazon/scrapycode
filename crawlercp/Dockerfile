FROM ubuntu:18.04
ENV TZ=Asia
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN  apt-get update -y --fix-missing
RUN  apt-get install -y python3 python3-pip python3-dev
RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org scrapy configparser requests lxml 
RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org boto3 requests_ntlm
RUN apt-get -y install curl
RUN apt-get -y install jq
RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org awscli
ADD crawlercp /
CMD ./SmartSpyder.sh
