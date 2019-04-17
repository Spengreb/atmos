#!/usr/bin/env python3

import argparse, subprocess, shlex, sys, os, glob

def main(argv):
    parser = argparse.ArgumentParser(description='Control Terraform Workspaces.')
    g = parser.add_mutually_exclusive_group()
    g.add_argument("command", help="Send commands to terraform with workspace variable context", nargs='?', default=False)
    parser.add_argument("-e", help="Template mode, gather shared-creds from environment variables (Dont use this flag if you dont want your ~/.aws/credentials replaced. This is for CI/CD", action='store_true', default=False)
    args, params = parser.parse_known_args()
    if args.command:
        determine_actions(args, params)

def determine_actions(args, params):
    workspace_manager()
    workspace = get_env()
    env_actions = ["plan", "apply", "destroy"] # Commands that require env context
    cmd = 'terraform {args}'.format(args=args.command)

    for param in params: # Pass terraform params directly through
        cmd = cmd + ' ' + param

    if (args.command in env_actions) and (workspace != "default"): # Append with env context
        cmd = cmd + ' -var-file=vars/{env}.tfvars -var "workspace={env}"'.format(env=workspace)

    if (args.e):
        generate_creds()
    
    print('Terraform {args} using env vars in {env}'.format(args=args.command, env=workspace))
    with subprocess.Popen(shlex.split(cmd)) as proc:
        exit # Start process but kill py program

def workspace_manager():
    if is_git_directory != False:
        branch = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
        if branch == "master":
            branch = "default"
        else:
            if branch not in get_valid_envs():
                branch = "qa"

        if get_env() != branch:
            print("WARNING: Terraform workspace & git branch have diverged. Changing workspace to git branch...")
            subprocess.call(["terraform", "workspace", "new", branch], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w'))
            subprocess.call(["terraform", "workspace", "select", branch], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w'))

def is_git_directory(path = '.'):
    if subprocess.call(["git", "branch"], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w')) != 0:
        return(False)
    else:
        return(True)

def generate_creds():
    current_workspace = get_env()
    workspaces = ['default']

    if current_workspace != 'default':
        workspaces.append(current_workspace)
    
    contents = ""
    for workspace in workspaces:
        contents = contents + "[{workspace}]\n".format(workspace=workspace)
        contents = contents + "aws_access_key_id=" + os.environ.get(workspace.upper() + '_ACCESS_KEY_ID') + "\n"
        contents = contents + "aws_secret_access_key=" + os.environ.get(workspace.upper() + '_SECRET_ACCESS_KEY') + "\n"
    with open(os.path.expanduser('~/.aws/credentials'), 'w+') as f:
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