# GitHub Repository Sync Setup Guide

This guide explains how to set up and sync this local repository with GitHub.

## Current Status

- ✅ Local git repository initialized
- ✅ Remote `origin` configured: `https://github.com/nlindmark/code_with_AI.git`
- ⏳ GitHub repository needs to be created (if not already exists)
- ⏳ Initial push needs to be performed

## Step-by-Step Setup

### Step 1: Create GitHub Repository

If the repository doesn't already exist on GitHub, create it:

1. Go to https://github.com/new
2. Repository name: `code_with_AI`
3. Description: (optional) "Code with AI - Tävlingsplattform"
4. Visibility: Choose Public or Private
5. **Do NOT** initialize with README, .gitignore, or license (we already have these locally)
6. Click "Create repository"

### Step 2: Verify Remote Configuration

Check that the remote is configured correctly:

```bash
git remote -v
```

You should see:
```
origin	https://github.com/nlindmark/code_with_AI.git (fetch)
origin	https://github.com/nlindmark/code_with_AI.git (push)
```

### Step 3: Authenticate with GitHub

You'll need to authenticate when pushing. You have two options:

#### Option A: Personal Access Token (HTTPS)

1. Create a Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Give it a name and select scopes: `repo` (full control of private repositories)
   - Copy the token

2. When pushing, Git will prompt for credentials:
   - Username: `nlindmark`
   - Password: `<paste your personal access token>`

#### Option B: SSH Key (Recommended for frequent use)

1. Generate SSH key (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Add SSH key to GitHub:
   - Copy your public key: `cat ~/.ssh/id_ed25519.pub`
   - Go to https://github.com/settings/keys
   - Click "New SSH key" and paste your public key

3. Update remote URL to use SSH:
   ```bash
   git remote set-url origin git@github.com:nlindmark/code_with_AI.git
   ```

### Step 4: Initial Push to GitHub

Push your local repository to GitHub:

```bash
# Push master branch
git push -u origin master
```

**Note**: If GitHub uses `main` as the default branch name:

```bash
# Option 1: Push master to main branch
git push -u origin master:main

# Option 2: Rename local branch to main first
git branch -M main
git push -u origin main
```

### Step 5: Verify Sync

After pushing, verify that everything is synced:

1. Visit https://github.com/nlindmark/code_with_AI
2. Check that all your files are present
3. Verify the commit history matches your local repository

## Ongoing Sync Workflow

### Making Changes and Syncing

1. **Stage your changes**:
   ```bash
   git add <files>        # Specific files
   # or
   git add -A            # All changes
   ```

2. **Commit your changes**:
   ```bash
   git commit -m "Descriptive commit message"
   ```

3. **Push to GitHub**:
   ```bash
   git push origin master    # or `main` if you renamed the branch
   ```

### Pulling Changes from GitHub

If you're working from multiple machines or with collaborators:

```bash
# Fetch and merge changes
git pull origin master

# Or fetch first to review changes
git fetch origin
git log HEAD..origin/master
git merge origin/master
```

## Troubleshooting

### "Repository not found" Error

- Ensure the repository exists on GitHub
- Check that you have the correct permissions
- Verify the remote URL: `git remote -v`

### "Authentication failed" Error

- Make sure you're using a Personal Access Token (not your password) for HTTPS
- For SSH, ensure your SSH key is added to GitHub and agent is running:
  ```bash
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_ed25519
  ```

### "Branch name mismatch" Error

- GitHub may use `main` while your local branch is `master`
- Use: `git push -u origin master:main` to push to the correct branch
- Or rename your local branch: `git branch -M main`

### "Updates were rejected" Error

- Someone else pushed changes, or you made changes on GitHub
- Pull first: `git pull origin master` (or `main`)
- Resolve any conflicts, then push again

## Files Excluded from Sync

The following files are excluded from git (via `.gitignore`):
- `*.db` files (database files)
- `__pycache__/` (Python cache)
- `.env` files (environment variables)
- Virtual environments (`.venv/`, `venv/`, etc.)
- IDE files (`.vscode/`, `.idea/`)

These files remain local-only for security and convenience.





