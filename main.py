import os
import shutil
import subprocess
import tempfile
import platform

import click


def create_new_repo():
    """Initialize a new temp Git repo and track its path and creator"""

    # Create a temporary directory
    repo_path = tempfile.mkdtemp(prefix="git_conflict_")
    print(repo_path)

    # Save repo path
    with open("repo_path.txt", "w") as f:
        f.write(repo_path)

    run_git_command(["init"], repo_path)
    run_git_command(["checkout", "-b", "main"], repo_path)

    print(f"Created new Git repo at {repo_path}")

def create_base_file():
    repo_path = get_repo_path()

    file_path = os.path.join(repo_path, "hello.txt")
    with open(file_path, "w") as f:
        f.write("")

    run_git_command(["add", "hello.txt"], repo_path)
    run_git_command(["commit", "-m", "Initial commit on main"], repo_path)

    print(f"Base file 'hello.txt' has been created and committed on 'main'.")
    return file_path

def make_change_on_branch():
    """ Prompt user input to 1) create a feature branch, and 2) make changes in the first 3 lines of 'hello.txt' file"""

    user_name, user_email = prompt_user_name()
    feature_branch_name = "feature-"+click.prompt("Branch to work on. Please type 'a' or 'b' ")
    print(f"Branch '{feature_branch_name}' has been created.")

    repo_path = get_repo_path()
    if not repo_path:
        print("No repo found. Please run 'initial-setup' first.")
        return

    # Switch to new feature branch
    run_git_command(["checkout", "-b", feature_branch_name], repo_path)

    line_1 = "Line 1" + click.prompt("Please type your input for Line 1 ")
    line_2 = "Line 2" + click.prompt("Please type your input for Line 2 ")
    line_3 = "Line 3" + click.prompt("Please type your input for Line 3 ")
    content = f"{line_1}\n{line_2}\n{line_3}"

    file_path = os.path.join(repo_path, "hello.txt")

    # Write changes in hello.txt file
    with open(file_path, "w") as f:
        f.write(content)

    # Log user and commit
    save_user_log("make_change_on_branch", feature_branch_name, user_name, user_email, content)

    # Stage and commit changes
    run_git_command(["add", "hello.txt"], repo_path)
    print(f"Changes on Feature branch '{feature_branch_name}' has been staged.")
    run_git_command(["commit", "-m", f"Edit the first three lines of file by {user_name}"], repo_path)
    print(f"Changes on branch '{feature_branch_name}' has been committed by {user_name}.")

    is_to_open = click.prompt("Do you want to open the file you've just made changes to? (y/n) ")
    if is_to_open == "y":
        open_hello_file()

def merge_two_branches():
    repo_path = get_repo_path()
    current_branch = get_current_branch(repo_path)

    if not current_branch:
        print("No branch found. Please run 'initial-setup' first.")
        return

    if current_branch == "main":
        print("You're currently on branch: main.")
        print("To create a merge conflict, please run 'make-changes' first.")

    branch_to_merge = "feature-a" if current_branch == "feature-b" else "feature-b"
    print(f"You're currently on branch: {current_branch}.")
    print(f"Merging {branch_to_merge} into {current_branch}...")

    result = run_git_command(["merge", branch_to_merge], repo_path)
    if "CONFLICT" in result.stdout or "Automatic merge failed" in result.stderr:
        print("Merge conflict detected. Please resolve conflict in the 'hello.txt' file.")
        print("Once the conflict is resolved, please call the 'complete-merge' command.")
    else:
        print("Merge attempt complete.")
    open_hello_file()

# Utility functions
def get_repo_path():
    try:
        with open("repo_path.txt", "r") as f:
            return f.readline().strip()
    except FileNotFoundError:
        print("Repo path not found.")
        return None

def open_hello_file():
    repo_path = get_repo_path()
    file_path = os.path.join(repo_path, "hello.txt")

    if not os.path.exists(file_path):
        print("'hello.txt' file not found.")
        return

    print(f"Opening '{file_path}'...")
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.run(["open", file_path])
    elif system == "Windows":
        subprocess.run(["start", "", file_path], shell=True)
    elif system == "Linux":
        subprocess.run(["xdg-open", file_path])
    else:
        print("Unsupported OS for auto-open.")

def prompt_user_name():
    user_name = click.prompt("Who is making this change?", default="Anonymous")
    user_email = f"{user_name.lower().replace(' ', '_')}@example.com"
    return user_name, user_email

def save_user_log(command, feature_branch, user_name, user_email, details):
    with open("user_log.txt", "a") as f:
        f.write(f"{command} | {feature_branch} | {user_name.lower()} | {user_email}\n Changes: \n {details}\n")

def get_current_branch(repo_path):
    result = run_git_command(["branch"], repo_path)
    for line in result.stdout.splitlines():
        if line.startswith("*"):
            return line.strip("* ").strip()
    return None

def run_git_command(args, repo_path):
    full_command = ["git"] + args
    result = subprocess.run(full_command, cwd=repo_path, capture_output=True, text=True)
    return result


@click.group()
def cli():
    pass

@cli.command()
def initial_setup():
    create_new_repo()
    file_path = create_base_file()
    print(f"Initial setup complete. An empty file called 'hello.txt' is created under the path {file_path}.")

@cli.command()
def make_changes():
    make_change_on_branch()

@cli.command()
def create_merge_conflict():
    merge_two_branches()

@cli.command()
def complete_merge():
    repo_path = get_repo_path()
    run_git_command(["add", "hello.txt"], repo_path)
    run_git_command(["commit"], repo_path)

    print("Merge completed successfully.")
    print("You can clean up the temp files by using the 'cleanup' command. Or restart the practice with 'initial-setup'. ")

@cli.command()
def cleanup():
    repo_path = get_repo_path()
    if repo_path and os.path.exists(repo_path):
        print("Removing 'hello.txt' file...")
        shutil.rmtree(repo_path)

    for state_file in ["repo_path.txt", "user_log.txt"]:
        if os.path.exists(state_file):
            print(f"Removing {state_file}")
            os.remove(state_file)


if __name__ == "__main__":
    cli()