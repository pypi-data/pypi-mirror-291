import os
import subprocess
from gai.lib.common.utils import root_dir

def docker_start(here):
    try:
        docker_compose_path = os.path.abspath(os.path.join(root_dir(),"docker-compose.yml"))
        print("docker-compose:",docker_compose_path)
        docker_command = f"docker-compose -f {docker_compose_path} up -d --force-recreate"
        subprocess.run(docker_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")