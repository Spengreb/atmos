import subprocess, os, glob

def workspace_manager():
    branch = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
    if branch == "master":
        branch = "default"
    else:
        if branch not in get_valid_envs():
            branch = "default"

    if get_env() != branch:
        print("[INFO]: Terraform workspace & git branch have diverged. Changing workspace to git branch...")
        subprocess.call(["terraform", "workspace", "new", branch], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w'))
        subprocess.call(["terraform", "workspace", "select", branch], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w'))

def get_valid_envs():
    try:
        # Use var files when present, otherwise default to default
        return [os.path.splitext(os.path.basename(x))[0] for x in glob.glob("vars/*.tfvars")]
    except FileNotFoundError:
        return False

def get_env():
    try:
        tf_env = ""
        with open('.terraform/environment', 'r') as f:
            tf_env = f.readline()
    except:
        return("default")
    if str(tf_env) in get_valid_envs():
        return(tf_env)
    else:
        return("default")