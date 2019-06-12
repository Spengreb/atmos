[![CircleCI](https://circleci.com/gh/Spengreb/atmos.svg?style=svg)](https://circleci.com/gh/Spengreb/atmos)
[![Build Status](https://cloud.drone.io/api/badges/Spengreb/atmos/status.svg)](https://cloud.drone.io/Spengreb/atmos)

# Terraform Atmosphere :earth_africa:
Atmos is a thin wrapper for managing Terraform Workspaces easily. Using the workspace name it will select the correct .tfvar file, defaulting to a qa var file for any other workspace. This is primarily for pipelines but works just as well from the command line. It can process all terraform commands and parameters passing them on directly. Atmos will automatically switch workspaces per git branches if it discovers its in a git repository

# Quick Start

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

Note: Atmos will override your default credentials file as this functionality is for use in a docker container or in situations where you would rather use variables.

# atmos -m

Adding `-m` flag will set to manual mode. It will not try to automatically switch workspace per branch. It will adhere to whatever you last set the workspace to.