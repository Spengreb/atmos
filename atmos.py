#!/usr/bin/env python3

import argparse, subprocess, shlex, sys, os, glob
import workspaces
import credentials

def main(argv):
    parser = argparse.ArgumentParser(description='Control Terraform Workspaces.')
    g = parser.add_mutually_exclusive_group()
    g.add_argument("command", help="Send commands to terraform with workspace variable context", nargs='?', default=False)
    parser.add_argument("-e", help="Gather shared-creds from environment variables (Dont use this flag if you dont want your ~/.aws/credentials replaced.) This is for CI/CD", action='store_true', default=False)
    parser.add_argument("-m", help="Prevents workspace from changing with git branches automatically", action='store_true', default=False)
    parser.add_argument("-n", help="Atmos will not add -var-file or -var args to terraform", action='store_true', default=False)
    parser.add_argument("-p", "--project", help="Add a project prefix for env vars", nargs='?', default="")
    parser.add_argument("-v", "--verbose", help="Debug mode", action="store_true", default=False)
    args, params = parser.parse_known_args()
    if args.command:
        determine_actions(args, params)

def determine_actions(args, params):
    aws_creds_file = "$HOME/.aws/credentials"
    if (is_git_directory()) and not (args.m):
        # if (args.e):
        #     aws_creds_file = aws_creds_file + "-atmos"
        workspaces.workspace_manager()

    workspace = workspaces.get_env()
    workspace_vars = workspace
    if (args.project) and workspace != 'default':
        workspace = args.project + "-" + workspace

    env_actions = ["init", "plan", "apply", "destroy"] # Commands that require env context
    cmd = 'terraform {args}'.format(args=args.command)

    if (args.command in env_actions) and not (args.n): # Append with env context
        cmd = cmd + ' -var-file=vars/{env}.tfvars'.format(env=workspace_vars) 
        cmd = cmd + ' -var "workspace={env}"'.format(env=workspace)
        cmd = cmd + ' -var "shared_credentials_file={aws_creds_file}"'.format(aws_creds_file=aws_creds_file)

    for param in params: # Pass terraform params directly through
        cmd = cmd + ' ' + param

    if (args.e):
        credentials.generate(args)

    if (args.verbose):
        print("Atmos will run: " + cmd)
    print('Terraform {args} using env vars in {env}'.format(args=args.command, env=workspace_vars))
    run_cmd(cmd)

def run_cmd(cmd):
    with subprocess.Popen(shlex.split(cmd)) as proc:
        exit # Start process but kill py program

def is_git_directory():
    return subprocess.call(['git', 'branch'], stderr=subprocess.STDOUT, stdout = open(os.devnull, 'w')) == 0


if __name__ == "__main__":
    main(sys.argv)