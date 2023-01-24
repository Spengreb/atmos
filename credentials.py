import workspaces, sys, os

def generate(args):
    current_workspace = workspaces.get_env()
    workspaces_names = ['default']
    aws_creds_dir = '~/.aws'
    aws_creds_file = 'credentials'
    aws_creds_full = aws_creds_dir + '/' + aws_creds_file

    if current_workspace != 'default':
        workspaces_names.append(current_workspace)

    project_name = ""
    if (args.project):
        delimeter = "_"
        project_name = args.project.upper() + delimeter

    contents = ""
    for workspace in workspaces_names:
        access_key_name = project_name + workspace.upper() + '_ACCESS_KEY_ID'
        secret_key_name = project_name + workspace.upper() + '_SECRET_ACCESS_KEY'

        if (args.verbose):
            print(access_key_name)
            print(secret_key_name)

        if (workspace == 'default'):
            contents = contents + "[{workspace}]\n".format(workspace=(workspace).lower())
        else:
            contents = contents + "[{workspace}]\n".format(workspace=(project_name.replace("_", "-") + workspace).lower())

        try:
            contents = contents + "aws_access_key_id=" + os.environ.get(access_key_name) + "\n"
        except:
            print("[ERROR]: Env Variable " + access_key_name + " not found.")
            sys.exit(1)
        try:
            contents = contents + "aws_secret_access_key=" + os.environ.get(secret_key_name) + "\n"
        except:
            print("[ERROR]: Env Variable " + secret_key_name + " not found.")
            sys.exit(1)

    if os.path.isfile(os.path.expanduser(aws_creds_full)):
        answer = input(f"[WARNING] File {aws_creds_full} already exists. Atmos will generate a new credentials file from your env vars. \nDo you want to override {aws_creds_full}? [y/N]")
        if not answer or answer[0].lower() != 'y':
            print("File not changed. This flag is for CI/CD only")
            exit(1)
    else:
        if not os.path.isdir(os.path.expanduser(aws_creds_dir)):
            os.makedirs(os.path.expanduser(aws_creds_dir))

    with open(os.path.expanduser(aws_creds_full), 'w+') as f:
        f.write(contents)
