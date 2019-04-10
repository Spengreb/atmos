# Terraform Atmosphere
Atmos is a thin wrapper for managing Terraform Workspaces easily. Using the workspace name it will select the correct .tfvar file, defaulting to a qa var file for any other workspace. This is primarily for pipelines but works just as well from the command line. It can process all terraform commands and parameters passing them directly to it.

# Quick Start

- Build the atmos image
- Use atmos as the build image in your CI/CD
- Include switching/creating terraform workspaces
- Use `$ atmos apply/plan/destroy` to run terraform apply whilst maintaining environment context