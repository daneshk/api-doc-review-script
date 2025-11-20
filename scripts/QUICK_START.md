# Quick Start Guide

Deploy the `/review-docs` command to multiple Ballerina repositories in 3 easy steps.

## Step 1: Create Repository List

```bash
cd scripts
cp repos-example.txt repos.txt
```

Edit `repos.txt` and add your repositories:
```
/Users/you/ballerina-platform/module-ballerinax-aws.s3
/Users/you/ballerina-platform/module-ballerinax-aws.lambda
https://github.com/ballerina-platform/module-ballerinax-aws.sns.git
```

## Step 2: Deploy

**Preview first (recommended):**
```bash
./deploy-docs-review-command.sh repos.txt --dry-run
```

**Deploy and commit:**
```bash
./deploy-docs-review-command.sh repos.txt --commit
```

**Deploy, commit, and push:**
```bash
./deploy-docs-review-command.sh repos.txt --commit --push
```

## Step 3: Use the Command

In any repository, open Claude Code and type:
```
/review-docs
```

## That's It! 🎉

The command will now analyze API documentation and provide improvements for low-code editor compatibility.

---

## Common Commands

| Task | Command |
|------|---------|
| Preview changes | `./deploy-docs-review-command.sh repos.txt --dry-run` |
| Deploy only | `./deploy-docs-review-command.sh repos.txt` |
| Deploy + commit | `./deploy-docs-review-command.sh repos.txt --commit` |
| Deploy + commit + push | `./deploy-docs-review-command.sh repos.txt --commit --push` |

## Need Help?

See [README.md](README.md) for detailed documentation and troubleshooting.
