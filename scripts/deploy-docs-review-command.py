#!/usr/bin/env python3

"""
Deploy API Documentation Review Command to Multiple Ballerina Repositories

This script deploys the /review-docs slash command to multiple repositories.
It can work with both local repositories and remote repositories (will clone).

Usage:
    python3 deploy-docs-review-command.py repos.txt
    python3 deploy-docs-review-command.py repos.txt --commit --push
    python3 deploy-docs-review-command.py repos.txt --dry-run
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple


class Colors:
    """ANSI color codes"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_colored(text: str, color: str):
    """Print colored text"""
    print(f"{color}{text}{Colors.NC}")


def run_command(cmd: List[str], cwd: str = None, capture_output: bool = True) -> Tuple[bool, str]:
    """Run a shell command and return success status and output"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=True
        )
        return True, result.stdout if capture_output else ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr if capture_output else ""


def is_git_repo(path: str) -> bool:
    """Check if directory is a git repository"""
    return os.path.isdir(os.path.join(path, '.git'))


def is_remote_url(repo_path: str) -> bool:
    """Check if path is a remote URL"""
    return repo_path.startswith('http://') or repo_path.startswith('https://') or repo_path.startswith('git@')


def clone_repository(repo_url: str, target_dir: str) -> bool:
    """Clone a git repository"""
    success, _ = run_command(['git', 'clone', repo_url, target_dir])
    return success


def read_repo_list(file_path: str) -> List[str]:
    """Read repository list from file, filtering comments and empty lines"""
    repos = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                repos.append(line)
    return repos


def process_repository(
    repo_path: str,
    prompt_source: str,
    temp_dir: str,
    do_commit: bool,
    do_push: bool,
    dry_run: bool
) -> Tuple[bool, str]:
    """
    Process a single repository
    Returns: (success: bool, message: str)
    """
    # Determine local path
    if is_remote_url(repo_path):
        repo_name = os.path.basename(repo_path).replace('.git', '')
        local_path = os.path.join(temp_dir, repo_name)

        print("  Cloning repository...")
        if dry_run:
            print(f"  [DRY RUN] Would clone: {repo_path} to {local_path}")
        else:
            if not clone_repository(repo_path, local_path):
                return False, "Failed to clone repository"
            print_colored("  ✓ Cloned successfully", Colors.GREEN)
    else:
        local_path = repo_path

        if not os.path.isdir(local_path):
            return False, f"Directory not found: {local_path}"

        if not is_git_repo(local_path):
            return False, f"Not a git repository: {local_path}"

    # Create .claude/commands directory
    claude_dir = os.path.join(local_path, '.claude', 'commands')
    target_file = os.path.join(claude_dir, 'review-docs.md')

    print("  Creating .claude/commands directory...")
    if dry_run:
        print(f"  [DRY RUN] Would create: {claude_dir}")
    else:
        os.makedirs(claude_dir, exist_ok=True)
        print_colored("  ✓ Directory ready", Colors.GREEN)

    # Copy the prompt file
    print("  Copying review-docs.md...")
    if dry_run:
        print(f"  [DRY RUN] Would copy: {prompt_source} -> {target_file}")
    else:
        shutil.copy2(prompt_source, target_file)
        print_colored("  ✓ File copied", Colors.GREEN)

    # Git operations
    if do_commit:
        os.chdir(local_path)

        # Check if there are changes
        has_changes, _ = run_command(['git', 'diff', '--quiet', target_file])
        has_staged_changes, _ = run_command(['git', 'diff', '--cached', '--quiet', target_file])

        if has_changes or has_staged_changes:
            print("  Committing changes...")
            if dry_run:
                print("  [DRY RUN] Would commit changes")
            else:
                run_command(['git', 'add', target_file])
                commit_msg = """Add API documentation review command

Add /review-docs slash command for consistent API documentation review
across Ballerina connectors for low-code editor compatibility.

Co-Authored-By: Claude <noreply@anthropic.com>"""

                run_command(['git', 'commit', '-m', commit_msg])
                print_colored("  ✓ Changes committed", Colors.GREEN)

                if do_push:
                    print("  Pushing changes...")
                    if dry_run:
                        print("  [DRY RUN] Would push to remote")
                    else:
                        success, _ = run_command(['git', 'push'])
                        if success:
                            print_colored("  ✓ Changes pushed", Colors.GREEN)
                        else:
                            print_colored("  ✗ Failed to push changes", Colors.RED)
        else:
            print_colored("  ⚠  No changes to commit (file already exists)", Colors.YELLOW)

    return True, "Repository processed successfully"


def main():
    parser = argparse.ArgumentParser(
        description='Deploy API documentation review command to multiple Ballerina repositories'
    )
    parser.add_argument('repo_list', help='File containing list of repositories')
    parser.add_argument('--commit', action='store_true', help='Commit the changes to git')
    parser.add_argument('--push', action='store_true', help='Push the changes to remote (requires --commit)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')

    args = parser.parse_args()

    if args.push:
        args.commit = True  # Push requires commit

    # Get script directory and prompt source
    script_dir = Path(__file__).parent.resolve()
    prompt_source = script_dir.parent / '.claude' / 'commands' / 'review-docs.md'

    # Validation
    if not os.path.isfile(args.repo_list):
        print_colored(f"Error: Repository list file not found: {args.repo_list}", Colors.RED)
        sys.exit(1)

    if not os.path.isfile(prompt_source):
        print_colored(f"Error: Source prompt file not found: {prompt_source}", Colors.RED)
        sys.exit(1)

    # Print header
    print_colored("=" * 50, Colors.BLUE)
    print_colored("Ballerina API Docs Review Command Deployment", Colors.BLUE)
    print_colored("=" * 50, Colors.BLUE)
    print()
    print_colored("Configuration:", Colors.YELLOW)
    print(f"  Repository list: {args.repo_list}")
    print(f"  Source prompt: {prompt_source}")
    print(f"  Commit changes: {args.commit}")
    print(f"  Push changes: {args.push}")
    print(f"  Dry run: {args.dry_run}")
    print()

    # Read repository list
    repos = read_repo_list(args.repo_list)
    if not repos:
        print_colored("Error: No repositories found in list file", Colors.RED)
        sys.exit(1)

    # Statistics
    total_repos = len(repos)
    successful_repos = 0
    failed_repos = 0

    # Create temporary directory for cloned repos
    with tempfile.TemporaryDirectory() as temp_dir:
        # Process each repository
        for idx, repo_path in enumerate(repos, 1):
            print_colored("-" * 50, Colors.BLUE)
            print_colored(f"[{idx}/{total_repos}] Processing: {repo_path}", Colors.BLUE)

            success, message = process_repository(
                repo_path,
                str(prompt_source),
                temp_dir,
                args.commit,
                args.push,
                args.dry_run
            )

            if success:
                print_colored(f"  ✓ {message}", Colors.GREEN)
                successful_repos += 1
            else:
                print_colored(f"  ✗ {message}", Colors.RED)
                failed_repos += 1

    # Summary
    print()
    print_colored("=" * 50, Colors.BLUE)
    print_colored("Deployment Summary", Colors.BLUE)
    print_colored("=" * 50, Colors.BLUE)
    print(f"  Total repositories: {total_repos}")
    print_colored(f"  Successful: {successful_repos}", Colors.GREEN)
    if failed_repos > 0:
        print_colored(f"  Failed: {failed_repos}", Colors.RED)
    print()

    if args.dry_run:
        print_colored("This was a dry run. No changes were made.", Colors.YELLOW)
        print("Run without --dry-run to apply changes.")
        print()

    if failed_repos > 0:
        sys.exit(1)

    print_colored("Deployment completed successfully!", Colors.GREEN)
    print()
    print("Next steps:")
    print("  1. Test the command in one repository: /review-docs")
    print("  2. If issues found, update the prompt and re-run this script")
    print("  3. Create PRs for the changes if needed")


if __name__ == '__main__':
    main()
