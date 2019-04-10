#!/usr/bin/env python3

import argparse, subprocess, shlex, sys, os

def main(argv):
    parser = argparse.ArgumentParser(description='Control Terraform Workspaces.')
    g = parser.add_mutually_exclusive_group()
    g.add_argument("command", help="Send commands to terraform with workspace variable context", nargs='?', default=False)
    g.add_argument("-configure", help="Setup atmos parameters", nargs='?', default=False)
    args, params = parser.parse_known_args()
    if args.command:
        determine_actions(args, params)
    if args.configure == None:
        configure_atmos()

def determine_actions(args, params):
    env_actions = ["plan", "apply", "destroy"] # Commands that require env context
    cmd = 'terraform {args}'.format(args=args.command)

    for param in params: # Pass terraform params directly through
        cmd = cmd + ' ' + param

    if args.command in env_actions: # Append with env context
        cmd = cmd + ' -var-file=vars/{env}.tfvars'.format(env=get_env())

    print('Terraform {args} using env vars in {env}'.format(args=args.command, env=get_env()))
    with subprocess.Popen(shlex.split(cmd)) as proc:
        exit # Start process but kill py program

def get_valid_envs():
    try:
        return open(os.path.expanduser('~/.config/atmos.config'), 'r').read().split(",")
    except FileNotFoundError:
        return False

def get_env():
    tf_env = subprocess.getoutput('cat .terraform/environment')
    if str(tf_env) in get_valid_envs():
        return(tf_env)
    else:
        return("qa")

def configure_atmos():
    current_valid_envs = get_valid_envs()
    if current_valid_envs:
        print("Current special environments: {envs}".format(envs=current_valid_envs))
    valid_envs = input("Enter special environments, e.g dev,preprod,prod: ")
    with open(os.path.expanduser('~/.config/atmos.config'),"w+") as f:
        f.write(valid_envs)

if __name__ == "__main__":
    main(sys.argv)