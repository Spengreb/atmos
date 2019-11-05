FROM ubuntu:xenial

RUN apt-get update -y && apt-get install -y python3 wget unzip git
RUN wget -O /tmp/terraform.zip https://releases.hashicorp.com/terraform/0.12.9/terraform_0.12.9_linux_amd64.zip
RUN unzip /tmp/terraform.zip 
RUN mv terraform /usr/bin/

COPY git-askpass-helper.sh /usr/bin/git-pass
COPY shared-creds /root/.aws/credentials
COPY atmos.py /usr/bin/atmos