# API Documentation Review Command Deployment

This directory contains scripts to deploy the `/review-docs` slash command to multiple Ballerina connector repositories for consistent API documentation review.

## 📁 Files

- **`deploy-docs-review-command.sh`** - Bash script for deployment
- **`deploy-docs-review-command.py`** - Python script for deployment (same functionality)
- **`repos-example.txt`** - Example repository list file
- **`../.claude/commands/review-docs.md`** - The documentation review prompt

## 🚀 Quick Start

### 1. Create Your Repository List

Copy the example file and add your repositories:

```bash
cp repos-example.txt repos.txt
# Edit repos.txt and add your repository paths
```

Example `repos.txt`:
```
# Local repositories
/Users/you/projects/module-ballerinax-aws.s3
/Users/you/projects/module-ballerinax-aws.lambda

# Remote repositories (will be cloned)
https://github.com/ballerina-platform/module-ballerinax-aws.sns.git
https://github.com/ballerina-platform/module-ballerinax-aws.sqs.git
```

### 2. Run the Deployment Script

**Option A: Bash Script (recommended for Unix/Linux/macOS)**
```bash
# Dry run (preview changes)
./deploy-docs-review-command.sh repos.txt --dry-run

# Deploy without committing
./deploy-docs-review-command.sh repos.txt

# Deploy and commit
./deploy-docs-review-command.sh repos.txt --commit

# Deploy, commit, and push
./deploy-docs-review-command.sh repos.txt --commit --push
```

**Option B: Python Script (cross-platform)**
```bash
# Dry run (preview changes)
python3 deploy-docs-review-command.py repos.txt --dry-run

# Deploy without committing
python3 deploy-docs-review-command.py repos.txt

# Deploy and commit
python3 deploy-docs-review-command.py repos.txt --commit

# Deploy, commit, and push
python3 deploy-docs-review-command.py repos.txt --commit --push
```

### 3. Test the Command

In any deployed repository, open Claude Code and type:
```
/review-docs
```

Claude will analyze the connector's API documentation and provide improvements based on the guidelines.

## 📝 Command Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview what would be done without making changes |
| `--commit` | Commit the changes to git with a standard message |
| `--push` | Push the changes to the remote repository (requires `--commit`) |

## 🔄 Update the Prompt

If you need to update the documentation review guidelines:

1. Edit `../.claude/commands/review-docs.md`
2. Re-run the deployment script to update all repositories
3. The script will only commit if there are actual changes

## 📊 What the Script Does

For each repository in your list:

1. ✅ Checks if it's a local path or remote URL
2. ✅ Clones remote repositories to a temporary directory
3. ✅ Creates `.claude/commands/` directory if it doesn't exist
4. ✅ Copies `review-docs.md` to the repository
5. ✅ Optionally commits and pushes changes

## 🎯 Use Cases

### Scenario 1: Add to All Existing Repositories

```bash
# Create list of all local connector repos
find ~/projects/ballerina-platform -name "module-ballerinax-*" -type d > repos.txt

# Deploy to all
./deploy-docs-review-command.sh repos.txt --commit --push
```

### Scenario 2: Add to Specific Repositories

```bash
# Create custom list
cat > repos.txt << EOF
/path/to/repo1
/path/to/repo2
https://github.com/org/repo3.git
EOF

# Deploy
./deploy-docs-review-command.sh repos.txt --commit
```

### Scenario 3: Test Before Committing

```bash
# First, do a dry run
./deploy-docs-review-command.sh repos.txt --dry-run

# If looks good, deploy without committing to test manually
./deploy-docs-review-command.sh repos.txt

# Test in one repository, then commit to all
./deploy-docs-review-command.sh repos.txt --commit
```

### Scenario 4: Update Existing Command

```bash
# Edit the prompt
vim ../.claude/commands/review-docs.md

# Re-deploy to all repositories
./deploy-docs-review-command.sh repos.txt --commit --push
```

## 🛠️ Troubleshooting

### Script fails with "Permission denied"

Make the script executable:
```bash
chmod +x deploy-docs-review-command.sh
chmod +x deploy-docs-review-command.py
```

### "Not a git repository" warning

The script skips non-git directories. Ensure your repositories are git-initialized:
```bash
cd /path/to/repo
git init
```

### Clone fails for remote repositories

Check:
- Internet connection
- Git credentials are configured
- Repository URL is correct
- You have access to the repository

### Changes not committed

If using `--commit`, ensure:
- You're on a branch (not detached HEAD)
- You have permissions to commit
- The working directory is clean

## 📋 Example Output

```
======================================
Ballerina API Docs Review Command Deployment
======================================

Configuration:
  Repository list: repos.txt
  Source prompt: ../.claude/commands/review-docs.md
  Commit changes: true
  Push changes: false
  Dry run: false

----------------------------------------
[1] Processing: /Users/you/projects/module-ballerinax-aws.s3
  Creating .claude/commands directory...
  ✓ Directory ready
  Copying review-docs.md...
  ✓ File copied
  Committing changes...
  ✓ Changes committed
  ✓ Repository processed successfully

[2] Processing: https://github.com/org/module-ballerinax-aws.sns.git
  Cloning repository...
  ✓ Cloned successfully
  Creating .claude/commands directory...
  ✓ Directory ready
  Copying review-docs.md...
  ✓ File copied
  Committing changes...
  ✓ Changes committed
  ✓ Repository processed successfully

======================================
Deployment Summary
======================================
  Total repositories: 2
  Successful: 2

Deployment completed successfully!

Next steps:
  1. Test the command in one repository: /review-docs
  2. If issues found, update the prompt and re-run this script
  3. Create PRs for the changes if needed
```

## 🔗 Integration with CI/CD

You can integrate this into your CI/CD pipeline:

```yaml
# .github/workflows/deploy-docs-command.yml
name: Deploy Docs Review Command

on:
  push:
    paths:
      - '.claude/commands/review-docs.md'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to all repos
        run: |
          ./scripts/deploy-docs-review-command.sh repos.txt --commit --push
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 📚 Documentation Guidelines

The `/review-docs` command enforces these key guidelines:

1. ✅ Simplify function descriptions - no code snippets
2. ✅ Add comprehensive enum value descriptions
3. ✅ Remove "Represents" prefix from records/enums
4. ✅ Replace "legacy parameter" with helpful alternatives
5. ✅ Keep valuable context (Valid Values, costs, limits)
6. ✅ Remove backticks from operation names (keep for field names)

See `../.claude/commands/review-docs.md` for complete guidelines.

## 🤝 Contributing

To improve the documentation guidelines:

1. Edit `../.claude/commands/review-docs.md`
2. Test in a sample repository
3. Re-deploy to all repositories
4. Submit PR with improvements

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review the script output for error messages
- Test with `--dry-run` first
- Verify git and file permissions
