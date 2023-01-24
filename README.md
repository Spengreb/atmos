[![CircleCI](https://circleci.com/gh/Spengreb/atmos.svg?style=svg)](https://circleci.com/gh/Spengreb/atmos)
[![Build Status](https://cloud.drone.io/api/badges/Spengreb/atmos/status.svg)](https://cloud.drone.io/Spengreb/atmos)

# Terraform Atmosphere :earth_africa:
Atmos is a thin wrapper for managing Terraform Workspaces easily. Using the workspace name it will select the correct .tfvar file, defaulting to a qa var file for any other workspace. This is primarily for pipelines but works just as well from the command line. It can process all terraform commands and parameters passing them on directly. Atmos will automatically switch workspaces per git branches if it discovers its in a git repository

# Quick Start

## Local Use

Atmos requires terraform to be installed on your system. 

- Clone this atmos project
- Symlink atmos.py to your /usr/bin/ `$ ln -s $(pwd)/atmos.py /usr/bin/atmos`
- Set up your `~/.aws/credentials` to include a `[default]` stanza which is where your S3 backend storage is. 
- Setup other stanzas in your credentials file for each environment you want. For example `[dev]` with your dev account IAM credentials
- You can also setup environment variables and use the -e flag. See below for more.
- Use `$ atmos apply/plan/destroy` to run terraform apply whilst maintaining environment context

## CI/CD

- Build the atmos image
- Use atmos as the build image in your CI/CD
- Include switching/creating terraform workspaces
- Use `$ atmos apply/plan/destroy` to run terraform apply whilst maintaining environment context

# Directory structure

Atmos requires the following file structure

```
├── main.tf
├── variables.tf
└── vars
    ├── dev.tfvars
    ├── preprod.tfvars
    ├── prod.tfvars
    └── qa.tfvars
```

The vars directory is scanned by atmos and matches the current workspace to the vars file. If the workspace is not found it defaults to the qa environment. This is to ensure qa branches are deployed similarily without having to create a var file for each new branch.

# AWS Credentials

To get the most out of Terraform workspaces it is recommended that the AWS provider uses the profile attribute.

```
# main.tf
provider "aws" {
    region = "${var.region}"
    profile = "${var.workspace}"
    shared_credentials_file = ${var.shared_credentials_file}
}
```

```
# variables.tf
variable "workspace" {
    type = "string"
    default = "default"
}
```

This will make Terraform lookup AWS credentials from the `~/.aws/credentials` file using the workspace name as the stanza name. For example the credentials file would look like the shared-creds file in this repo.

## atmos -e

Adding the `-e` flag to atmos will make it generate a new `~/.aws/credentials` file from environment variables. You must first include the `default` access key ID & secret access key like this:

```
DEFAULT_ACCESS_KEY_ID=id
DEFAULT_SECRET_ACCESS_KEY=key
```

All additional workspaces need to be prefixed in the same way:

```
DEV_ACCESS_KEY_ID=id
DEV_SECRET_ACCESS_KEY=key

QA_ACCESS_KEY_ID=id
QA_SECRET_ACCESS_KEY=key
```

# atmos -m

Adding `-m` flag will set to manual mode. It will not try to automatically switch workspace per branch. It will adhere to whatever you last set the workspace to.

# atmos -p 

Adding `-p` flag will set the project prefix when looking for credentials. 

Example:
` $ atmos -e -p PROJ plan`

Will make atmos look for environment vars with the prefix 'VER' selecting the following env vars. 

```
PROJ_DEV_ACCESS_KEY_ID
PROJ_DEV_SECRET_ACCESS_KEY
```

Note this also works on the `.aws/credentials` file

# atmos -v

Verbose output mode, will show the vars atmos has selected and some environment context
