# acts as entry point for scripts to run in devcontainer

import experiments as exp
import os
import sys

def hello_world_test():
    with exp.working_directory(exp.project_root):
        with open("out.out", "w") as f:
            f.write("Devcontainer hello world")

        print("print hello world?")

def score_all_questions_test():
    with exp.working_directory(exp.devcontainer_root/"evaluation"):
        sys.path.append(os.getcwd()) 
        import score_all_questions as saq
        saq.main()

if __name__ == "__main__":
    os.environ['WORKSPACE_FOLDER'] = str(exp.devcontainer_root)

