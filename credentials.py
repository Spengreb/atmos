def generate(args):
    current_workspace = workspaces.get_env()
    workspaces_names = ['default']

    if current_workspace != 'default':
        workspaces_names.append(current_workspace)

    project_name = ""
    if (args.project):
        delimeter = "-"
        if (args.e):
            delimeter = "_"
        project_name = args.project.upper() + delimeter

    contents = ""
    for workspace in workspaces_names:
        access_key_name = project_name + workspace.upper() + '_ACCESS_KEY_ID'
        secret_key_name = project_name + workspace.upper() + '_SECRET_ACCESS_KEY'

        if (args.verbose):
            print(access_key_name)
            print(secret_key_name)

        contents = contents + "[{workspace}]\n".format(workspace=project_name + workspace)
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
    with open(os.path.expanduser('~/.aws/credentials'), 'w+') as f:
        f.write(contents)
