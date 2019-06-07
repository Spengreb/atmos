FROM ubuntu:xenial

RUN apt-get update -y && apt-get install -y python3 wget unzip git
RUN wget -O /tmp/terraform.zip https://releases.hashicorp.com/terraform/0.12.0/terraform_0.12.0_linux_amd64.zip
RUN unzip /tmp/terraform.zip 
RUN mv terraform /usr/bin/

COPY shared-creds /root/.aws/credentials
COPY atmos.py /usr/bin/atmos