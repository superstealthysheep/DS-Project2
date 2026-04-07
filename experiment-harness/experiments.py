# to be run from host machine, from the project root

import contextlib
import subprocess
import functools
import pathlib
import os

VERBOSE = True
project_name = "project2"
docker = "podman"
# docker = "docker"

@contextlib.contextmanager
def working_directory(path: pathlib.Path):
    origin = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)

def shell(command, **kwargs) -> str:
    if 'env' in kwargs:
        v_print(f"running following command with env: {kwargs['env']}")
    v_print("$ " + " ".join(map(str, command)))
    res = subprocess.run(command, capture_output=True, text=True, **kwargs)
    v_print(res.stderr, end="")
    v_print(res.stdout, end="")
    return res.stdout

# naming convention for vscode devcontainer docker images
image_pfx = f"localhost/vsc-{project_name}"

project_root = pathlib.Path(".")
devcontainer_root = pathlib.Path(f"/workspaces/{project_name}")
experiment_dir = project_root/"experiment-harness"
docker_dir = project_root/"docker"

def v_print(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

@functools.cache
def get_devcontainer_id():
    command = [docker, "ps", "-aq", "--filter", f"ancestor={image_pfx}"]
    res = shell(command)
    # v_print(" ".join(command))
    # res = subprocess.run(command, capture_output=True, text=True)
    # v_print(res.stdout, end="")
    devcontainer_id = res.strip()
    return devcontainer_id

# --------------------

def cleanup():
    with working_directory(docker_dir):
        shell(["docker", "compose", "down"])
        storage_node_ids = shell(["docker", "ps", "-aq", "--filter", "name=storage-node"])
        storage_node_ids = storage_node_ids.split()
        shell(["docker", "rm", "-f"] + storage_node_ids)

def build(max_vectors_per_node=1000):
    cleanup()
    with working_directory(docker_dir):
        shell(
            ["docker", "compose", "up", "--build", "-d"], 
            env=dict(MAX_VECTORS_PER_NODE=str(max_vectors_per_node)),
        )

# def send_command(container_id, command):
#     wrapped_cmd = [docker, "exec", ]

if __name__ == "__main__":
    # print(get_devcontainer_id())
    print("attempting build")
    # shell([f"docker", "exec", "-e", "MAX_VECTORS_PER_NODE={max_vectors_per_node}"])

    for max_vectors_per_node in [100, 200]:
        # build(max_vectors_per_node=max_vectors_per_node)
        shell([docker, "exec", "-w", devcontainer_root, get_devcontainer_id(), "python", "experiment-harness/devcontainer.py"], 
            #   env=dict(WORKING_DIRECTORY=pathlib.Path("/workspaces/"))
              )