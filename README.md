[![CircleCI](https://circleci.com/gh/Spengreb/atmos.svg?style=svg)](https://circleci.com/gh/Spengreb/atmos)

# Terraform Atmosphere
Atmos is a thin wrapper for managing Terraform Workspaces easily. Using the workspace name it will select the correct .tfvar file, defaulting to a qa var file for any other workspace. This is primarily for pipelines but works just as well from the command line. It can process all terraform commands and parameters passing them on directly.

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
provider "aws" {
    region = "${var.region}"
    profile = "${terraform.workspace}"
}
```

This will make Terraform lookup AWS credentials from the `~/.aws/credentials` file using the workspace name as the stanza name. For example the credentials file would look like the shared-creds file in this repo.
