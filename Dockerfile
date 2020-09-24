FROM ubuntu:xenial

RUN apt-get update -y && apt-get install -y python3 wget unzip git
RUN wget -O /tmp/terraform.zip https://releases.hashicorp.com/terraform/0.12.24/terraform_0.12.24_linux_amd64.zip
RUN unzip /tmp/terraform.zip 
RUN mv terraform /usr/bin/

COPY git-askpass-helper.sh /usr/bin/git-pass

RUN mkdir /atmos
COPY atmos.py credentials.py workspaces.py /atmos/
RUN ln -s /atmos/atmos.py /usr/bin/atmos
