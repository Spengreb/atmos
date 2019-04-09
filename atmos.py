#!/usr/bin/env python3

import argparse
import subprocess
import sys

def main(argv):
    parser = argparse.ArgumentParser(description='Control Terraform Workspaces.')
    parser.add_argument("command", help="Send commands to terraform", default=False)
    parser.add_argument("-auto", help="Flag to skip waiting for user input", action="store_true")
    args = parser.parse_args()
    determine_actions(args)

def determine_actions(args):
    if args.auto:
        args.command = args.command + " -auto-approve"
    valid_actions = ["plan", "apply", "destroy"]
    if args.command in valid_actions:
        print('Terraform {args} using env vars in {env}'.format(args=args.command, env=get_env()))
        print(subprocess.getoutput('terraform {args} -var-file=vars/{env}.tfvars'.format(args=args.command, env=get_env())))
    else:
        print(subprocess.getoutput('terraform {args}'.format(args=args.command)))

def get_env():
    valid_envs = ["dev","preprod","emea","apac"]
    tf_env = subprocess.getoutput('cat .terraform/environment')
    if str(tf_env) in valid_envs:
        return(tf_env)
    else:
        return("qa")

if __name__ == "__main__":
    main(sys.argv)