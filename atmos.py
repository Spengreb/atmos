#!/usr/bin/env python3

import argparse, subprocess, shlex, sys, os, glob

def main(argv):
    parser = argparse.ArgumentParser(description='Control Terraform Workspaces.')
    g = parser.add_mutually_exclusive_group()
    g.add_argument("command", help="Send commands to terraform with workspace variable context", nargs='?', default=False)
    args, params = parser.parse_known_args()
    if args.command:
        determine_actions(args, params)

def determine_actions(args, params):
    env_actions = ["plan", "apply", "destroy"] # Commands that require env context
    cmd = 'terraform {args}'.format(args=args.command)

    for param in params: # Pass terraform params directly through
        cmd = cmd + ' ' + param

    if (args.command in env_actions) and (get_env() != "master"): # Append with env context
        cmd = cmd + ' -var-file=vars/{env}.tfvars'.format(env=get_env())

    print('Terraform {args} using env vars in {env}'.format(args=args.command, env=get_env()))
    with subprocess.Popen(shlex.split(cmd)) as proc:
        exit # Start process but kill py program

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
        return("master")
    if str(tf_env) in get_valid_envs():
        return(tf_env)
    else:
        return("qa")

if __name__ == "__main__":
    main(sys.argv)