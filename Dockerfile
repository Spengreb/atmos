FROM python:latest

RUN apt update && apt install -y jq
RUN wget -O /tmp/terraform.zip `echo "https://releases.hashicorp.com/terraform/$(curl -s https://checkpoint-api.hashicorp.com/v1/check/terraform | jq -r -M '.current_version')/terraform_$(curl -s https://checkpoint-api.hashicorp.com/v1/check/terraform | jq -r -M '.current_version')_linux_amd64.zip"`
RUN unzip /tmp/terraform.zip 
RUN mv terraform /usr/bin/

COPY git-askpass-helper.sh /usr/bin/git-pass

RUN mkdir /atmos
COPY atmos.py credentials.py workspaces.py /atmos/
RUN ln -s /atmos/atmos.py /usr/bin/atmos
