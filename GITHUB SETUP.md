# 🚀 OCRS Backend - GitHub Repository Setup Guide

## Step 1: Create GitHub Repository

### Option A: Via GitHub Website (Recommended for Teams)

1. **Go to GitHub** and log in: https://github.com

2. **Create New Repository**:
   - Click the `+` icon in the top right
   - Select "New repository"

3. **Configure Repository**:
   ```
   Repository name: ocrs-backend
   Description: Online Course Registration System - Backend API
   Visibility: Private (recommended for team projects)
   
   ⚠️ DO NOT initialize with:
   - ❌ README
   - ❌ .gitignore
   - ❌ License
   (We already have these files!)
   ```

4. **Click "Create repository"**

5. **Copy the repository URL** (you'll need this):
   ```
   https://github.com/YOUR-USERNAME/ocrs-backend.git
   ```

### Option B: Via GitHub CLI (If installed)

```bash
# Create repository
gh repo create ocrs-backend --private --source=. --remote=origin

# Push code
git push -u origin main
```

## Step 2: Initialize Git and Push Code

Once you have the repository URL, follow these steps:

### On Your Local Machine

```bash
# 1. Navigate to the project directory
cd ocrs-backend

# 2. Initialize git repository
git init

# 3. Add all files
git add .

# 4. Create first commit
git commit -m "Initial commit: OCRS Backend Phase 1 - Database foundation complete

- Complete MySQL schema with 14 tables
- Database triggers and constraints
- Seed data with sample users and courses
- Flask application with JWT authentication
- Configuration management system
- Database connection utilities
- Input validation system
- Logging and response utilities
- Swagger API documentation setup
- Automated database setup script
- Comprehensive documentation"

# 5. Rename branch to main (if needed)
git branch -M main

# 6. Add remote repository (replace with YOUR repository URL)
git remote add origin https://github.com/YOUR-USERNAME/ocrs-backend.git

# 7. Push to GitHub
git push -u origin main
```

## Step 3: Verify Upload

1. Go to your GitHub repository URL
2. You should see all the files uploaded
3. Check that README.md displays correctly

## Step 4: Set Up Branch Protection (Recommended)

To protect your main branch and require code reviews:

1. Go to your repository on GitHub
2. Click "Settings"
3. Click "Branches" in the left sidebar
4. Click "Add rule" under "Branch protection rules"
5. Configure:
   ```
   Branch name pattern: main
   
   ✅ Require pull request reviews before merging
   ✅ Require status checks to pass before merging
   ✅ Require branches to be up to date before merging
   
   Number of required approvals: 1
   ```
6. Click "Create"

## Step 5: Team Collaboration Setup

### Add Team Members

1. Go to repository Settings
2. Click "Collaborators and teams"
3. Click "Add people"
4. Enter each team member's GitHub username:
   - Maurice Adovoekpe
   - Mansour Cheyo
   - Nelvis Lumvalla
   - Sritej Nadella
   - Steven Nguyen
   - Michael Sibley Jr.
   - Xu Wang
   - Ronell Wilder
   - Christopher Davis

### Set Up GitHub Projects (Optional)

1. Go to "Projects" tab
2. Click "New project"
3. Choose "Board" template
4. Name it "OCRS Development"
5. Add columns:
   - Backlog
   - To Do
   - In Progress
   - Review
   - Done

## Step 6: Create Initial Issues

Create issues for upcoming work:

```markdown
### Issue 1: Implement Authentication Module
**Labels**: enhancement, phase-2
**Assignee**: [Team Member]

Implement user authentication endpoints:
- [ ] POST /api/auth/register
- [ ] POST /api/auth/login
- [ ] POST /api/auth/logout
- [ ] POST /api/auth/refresh
- [ ] Unit tests

### Issue 2: Implement Course Management APIs
**Labels**: enhancement, phase-3
**Assignee**: [Team Member]

Build course management endpoints:
- [ ] GET /api/courses
- [ ] GET /api/courses/:id
- [ ] POST /api/courses (admin)
- [ ] PUT /api/courses/:id (admin)
- [ ] DELETE /api/courses/:id (admin)

### Issue 3: Set Up CI/CD Pipeline
**Labels**: infrastructure
**Assignee**: [Team Member]

Configure automated testing and deployment:
- [ ] GitHub Actions workflow
- [ ] Automated tests on PR
- [ ] Code coverage reporting
```

## Common Commands for Team Members

### Starting Work on a Feature

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create feature branch
git checkout -b feature/authentication
# or
git checkout -b feature/course-api
# or
git checkout -b fix/bug-description

# 3. Make changes and commit
git add .
git commit -m "Add authentication endpoints"

# 4. Push branch
git push origin feature/authentication

# 5. Create Pull Request on GitHub
```

### Updating Your Branch

```bash
# Get latest changes from main
git checkout main
git pull origin main

# Update your feature branch
git checkout feature/your-feature
git merge main

# Or use rebase (cleaner history)
git rebase main
```

### Branch Naming Convention

```
feature/   - New features (feature/enrollment-system)
fix/       - Bug fixes (fix/login-validation)
docs/      - Documentation updates (docs/api-guide)
refactor/  - Code refactoring (refactor/database-layer)
test/      - Adding tests (test/auth-module)
```

## Troubleshooting

### Problem: "remote origin already exists"

```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/YOUR-USERNAME/ocrs-backend.git
```

### Problem: "failed to push some refs"

```bash
# Pull first, then push
git pull origin main --allow-unrelated-histories
git push origin main
```

### Problem: Accidentally committed .env file

```bash
# Remove from git (but keep locally)
git rm --cached .env

# Add to .gitignore (already done)
echo ".env" >> .gitignore

# Commit the change
git add .gitignore
git commit -m "Remove .env from git tracking"
git push origin main
```

## Security Best Practices

### ⚠️ NEVER Commit:
- `.env` file with real credentials
- Database passwords
- API keys or secrets
- JWT secret keys

### ✅ ALWAYS:
- Use `.env.example` as template
- Keep `.env` in `.gitignore`
- Rotate secrets if accidentally committed
- Use environment variables for sensitive data

## Setting Up GitHub Secrets (For CI/CD)

If you set up GitHub Actions later:

1. Go to repository Settings
2. Click "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add secrets:
   ```
   DB_PASSWORD
   JWT_SECRET_KEY
   SECRET_KEY
   ```

## Quick Reference

```bash
# Check current status
git status

# View commit history
git log --oneline

# See all branches
git branch -a

# Switch branches
git checkout branch-name

# Pull latest changes
git pull origin main

# Push your changes
git push origin your-branch-name

# Create pull request
# Go to GitHub and click "Compare & pull request"
```

## Next Steps After Setup

1. ✅ All team members clone the repository
2. ✅ Set up local development environment (follow QUICKSTART.md)
3. ✅ Each member creates a test branch to verify access
4. ✅ Start working on Phase 2 tasks from TODO.md

## Team Workflow Recommendation

1. **Daily standup** - Share what you're working on
2. **Create branch** - For each feature/fix
3. **Make changes** - Work on your branch
4. **Create PR** - When ready for review
5. **Code review** - At least one team member reviews
6. **Merge** - After approval, merge to main
7. **Deploy** - Automated or manual deployment

---

## 📞 Need Help?

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com
- **Team Lead**: Christopher Davis

---

**Happy Collaborating! 🎉**