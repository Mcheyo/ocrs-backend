#!/bin/bash
# ============================================================================
# OCRS Backend - Git Initialization Script
# ============================================================================

echo "============================================================"
echo "🚀 OCRS Backend - Git Repository Initialization"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed. Please install Git first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Git is installed${NC}"
echo ""

# Check if already a git repository
if [ -d .git ]; then
    echo -e "${YELLOW}⚠️  This directory is already a git repository.${NC}"
    read -p "Do you want to reinitialize? (yes/no): " reinit
    if [ "$reinit" != "yes" ]; then
        echo "Cancelled."
        exit 0
    fi
    rm -rf .git
fi

# Initialize git repository
echo "📦 Initializing git repository..."
git init
echo -e "${GREEN}✅ Git repository initialized${NC}"
echo ""

# Add all files
echo "📝 Adding files..."
git add .
echo -e "${GREEN}✅ Files added${NC}"
echo ""

# Create initial commit
echo "💾 Creating initial commit..."
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

echo -e "${GREEN}✅ Initial commit created${NC}"
echo ""

# Rename branch to main
echo "🔀 Renaming branch to main..."
git branch -M main
echo -e "${GREEN}✅ Branch renamed to main${NC}"
echo ""

# Ask for remote repository URL
echo "============================================================"
echo "📡 GitHub Repository Setup"
echo "============================================================"
echo ""
echo "First, create a repository on GitHub:"
echo "  1. Go to https://github.com"
echo "  2. Click '+' -> 'New repository'"
echo "  3. Name it: ocrs-backend"
echo "  4. Make it Private"
echo "  5. DON'T initialize with README, .gitignore, or license"
echo "  6. Click 'Create repository'"
echo ""

read -p "Have you created the GitHub repository? (yes/no): " created
if [ "$created" != "yes" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Please create the GitHub repository first, then run this script again.${NC}"
    exit 0
fi

echo ""
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/ocrs-backend.git): " repo_url

if [ -z "$repo_url" ]; then
    echo -e "${RED}❌ No URL provided${NC}"
    exit 1
fi

# Add remote
echo ""
echo "🔗 Adding remote repository..."
git remote add origin "$repo_url"
echo -e "${GREEN}✅ Remote added${NC}"
echo ""

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
echo "This may prompt for your GitHub credentials..."
echo ""

if git push -u origin main; then
    echo ""
    echo "============================================================"
    echo -e "${GREEN}✅ SUCCESS! Repository pushed to GitHub${NC}"
    echo "============================================================"
    echo ""
    echo "🎉 Your code is now on GitHub!"
    echo ""
    echo "Next steps:"
    echo "  1. View your repository: ${repo_url%.git}"
    echo "  2. Add team members as collaborators"
    echo "  3. Set up branch protection (see GITHUB_SETUP.md)"
    echo "  4. Team members can now clone: git clone $repo_url"
    echo ""
    echo "📚 For detailed GitHub setup: See GITHUB_SETUP.md"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Push failed${NC}"
    echo ""
    echo "Possible reasons:"
    echo "  1. Authentication failed - check your GitHub credentials"
    echo "  2. Repository URL is incorrect"
    echo "  3. Repository already has content"
    echo ""
    echo "To try again manually:"
    echo "  git push -u origin main"
    echo ""
    echo "For help, see GITHUB_SETUP.md"
fi