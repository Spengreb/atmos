#!/usr/bin/env python3

import argparse, subprocess, shlex, sys, os, glob

def main(argv):
    parser = argparse.ArgumentParser(description='Control Terraform Workspaces.')
    g = parser.add_mutually_exclusive_group()
    g.add_argument("command", help="Send commands to terraform with workspace variable context", nargs='?', default=False)
    parser.add_argument("-e", help="Gather shared-creds from environment variables (Dont use this flag if you dont want your ~/.aws/credentials replaced. This is for CI/CD", action='store_true', default=False)
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
        if (args.e):
            aws_creds_file = aws_creds_file + "-atmos"
        workspace_manager()

    if (args.project) and (args.verbose):
        print("Project: " + args.project)

    workspace = get_env()
    env_actions = ["plan", "apply", "destroy"] # Commands that require env context
    cmd = 'terraform {args}'.format(args=args.command)

    if (args.command in env_actions) and not (args.n): # Append with env context
        cmd = cmd + ' -var-file=vars/{env}.tfvars -var "workspace={env}"'.format(env=workspace)
        cmd = cmd + ' -var "shared_credentials_file={aws_creds_file}"'.format(aws_creds_file=aws_creds_file)

    for param in params: # Pass terraform params directly through
        cmd = cmd + ' ' + param

    if (args.e):
        generate_creds(args)

    if (args.verbose):
        print("Atmos will run: " + cmd)

    print('Terraform {args} using env vars in {env}'.format(args=args.command, env=workspace))
    with subprocess.Popen(shlex.split(cmd)) as proc:
        exit # Start process but kill py program

def is_git_directory(path = '.'):
    return subprocess.call(['git', '-C', path, 'status'], stderr=subprocess.STDOUT, stdout = open(os.devnull, 'w')) == 0

def workspace_manager():
    branch = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
    if branch == "master":
        branch = "default"
    else:
        if branch not in get_valid_envs():
            branch = "qa"

    if get_env() != branch:
        print("[INFO]: Terraform workspace & git branch have diverged. Changing workspace to git branch...")
        subprocess.call(["terraform", "workspace", "new", branch], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w'))
        subprocess.call(["terraform", "workspace", "select", branch], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w'))

def generate_creds(args):
    current_workspace = get_env()
    workspaces = ['default']

    if current_workspace != 'default':
        workspaces.append(current_workspace)

    project_name = ""
    if (args.project):
        project_name = args.project.upper() + "_"

    contents = ""
    for workspace in workspaces:
        access_key_name = project_name + workspace.upper() + '_ACCESS_KEY_ID'
        secret_key_name = project_name + workspace.upper() + '_SECRET_ACCESS_KEY'

        if (args.verbose):
            print(access_key_name)
            print(secret_key_name)

        contents = contents + "[{workspace}]\n".format(workspace=workspace)
        contents = contents + "aws_access_key_id=" + os.environ.get(access_key_name) + "\n"
        contents = contents + "aws_secret_access_key=" + os.environ.get(secret_key_name) + "\n"
    with open(os.path.expanduser('~/.aws/credentials-atmos'), 'w+') as f:
        f.write(contents)

def get_valid_envs():
    try:
        # Use var files when present, otherwise default to qa
        return [os.path.splitext(os.path.basename(x))[0] for x in glob.glob("vars/*.tfvars")]
    except FileNotFoundError:
        return False

def get_env():
    try:
        tf_env = open('.terraform/environment', 'r').read()
    except:
        return("default")
    if str(tf_env) in get_valid_envs():
        return(tf_env)
    else:
        return("qa")

if __name__ == "__main__":
    main(sys.argv)