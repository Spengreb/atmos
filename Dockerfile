FROM ubuntu:xenial

RUN apk add python3
RUN wget -O /tmp/terraform.zip https://releases.hashicorp.com/terraform/0.11.13/terraform_0.11.13_linux_amd64.zip 
RUN unzip /tmp/terraform.zip 
RUN mv terraform /usr/bin/

COPY shared-creds /root/.aws/credentials
COPY atmos.py /usr/bin/atmos