# acts as entry point for scripts to run in devcontainer

import experiments as exp
import os

def hello_world_test():
    with exp.working_directory(exp.project_root):
        with open("out.out", "w") as f:
            f.write("Devcontainer hello world")

        print("print hello world?")

if __name__ == "__main__":
    with exp.working_directory(exp.project_root/"evaluation"):
        exp.shell(["python", "evaluate.py"], env=os.environ | dict(WORKSPACE_FOLDER=exp.devcontainer_root))