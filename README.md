# Git Conflict Trainer

**Git Conflict Trainer** is a Python-based CLI tool that simulates merge conflict scenarios inside a sandboxed Git repository. It helps learners safely practice resolving merge conflicts without touching real codebases.

---

## Features

- Simulates real Git merge conflicts
- Interactive CLI prompts
- Tracks changes in a temporary Git repo
- Safe and disposable (cleans up after use)
- Step-by-step training-style guidance

---

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/git-conflict-trainer.git
   cd git-conflict-trainer
2. Install the required Python dependency:
    ```bash
    pip install click
    ```
3. Run all commands from the terminal inside this folder:
    ```bash
    python main.py <command>
    ```

## Commands
This Cli includes five core commands:

| Command                 | Description                                                                |
| ----------------------- | -------------------------------------------------------------------------- |
| `initial-setup`         | Sets up a temporary Git repo with a `main` branch and an empty `hello.txt` |
| `make-changes`          | Prompts user input to create a feature branch and modify `hello.txt`       |
| `create-merge-conflict` | Simulates a merge conflict by merging one feature branch into another      |
| `complete-merge`        | Finalizes a merge after you've manually resolved the conflict              |
| `cleanup`               | Deletes the temporary repo and all associated tracking files               |


## Walkthrough: How to Use
This tool is designed to help you see and resolve a real Git merge conflict safely. Here’s how:

### Step 1: Set up a clean Git environment
```bash
python main.py initial-setup
```
This creates:
- A temp directory
- A Git repo with a `main` branch
- A tracked file: `hello.txt`

### Step 2: Simulate conflicting changes from two users
First user(feature-a)
```bash
python main.py make-changes
# user-1
# branch: feature-a
# line 3: user-1
```
After committing, return to main before simulating another change:
```bash
cd $(cat repo_path.txt)
git checkout main
```
Second user(feature-b)
```bash
python main.py make-changes
# user-2
# branch: feature-b
# line 3: user-2
```
Now you have two branches with different commits on the same line of hello.txt.

### Step 3: Create the merge conflict
```angular2html
python main.py create-merge-conflict
```
You’ll see a CONFLICT message and hello.txt will contain Git conflict markers (e.g., <<<<<<<, =======, >>>>>>>).

### Step 4: Resolve the conflict
Open hello.txt and manually resolve the conflict by choosing:
- One version (e.g., user-1's or user-2's)
- Or a combined version
Delete the Git conflict markers and save the file.

### Step 5: Complete the merge
Once the conflict is resolved, finish the merge:
```bash
python main.py complete-merge
```
This command stages the file and creates the merge commit.

### Step 6 Clean up 
To delete the temporary repo and reset the environment:
```bash
python main.py cleanup
```

## Why Use This?
Git conflicts can be confusing at first. This tool helps you:
- Understand how conflicts happen
- Practice resolving them safely
- Learn branching and merge fundamentals