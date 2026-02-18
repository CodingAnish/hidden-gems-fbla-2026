# Push to GitHub - Next Steps

Your local repository is ready! Now push it to GitHub.

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Repository name: `hidden-gems-fbla-2026`
3. Description: `A desktop app for discovering hidden gem businesses`
4. **Do NOT initialize** with README, .gitignore, or license
5. Click **Create repository**

## Step 2: Connect Remote & Push

Copy and run these commands:

```bash
cd /Users/anishranga/Downloads/hidden-gems-fbla-2026-main

# Replace USERNAME with your GitHub username
git remote add origin https://github.com/USERNAME/hidden-gems-fbla-2026.git
git branch -M main
git push -u origin main
```

**Using SSH?**
```bash
git remote add origin git@github.com:USERNAME/hidden-gems-fbla-2026.git
git branch -M main
git push -u origin main
```

## Step 3: Share the Link

Once pushed, your repo will be at:
```
https://github.com/USERNAME/hidden-gems-fbla-2026
```

Others can clone with:
```bash
git clone https://github.com/USERNAME/hidden-gems-fbla-2026.git
cd hidden-gems-fbla-2026-main
npm install
npm run dev
```

## What's Included

✅ Full source code
✅ All dependencies (requirements.txt, package.json)
✅ README with setup instructions
✅ Database setup (auto-seeds on first run)
✅ Environment template (.env.example)
✅ Git ignore configured

## What's NOT Included

❌ `.env` key file (users must create their own)
❌ `hidden_gems.db` (created automatically)
❌ `node_modules/` and `src-tauri/target/` (installed via `npm install`)

## Tips for Sharing

1. **Add collaborators** - Settings → Collaborators → Add
2. **Set up branch protection** - Require PR reviews for `main`
3. **Add GitHub Actions** - Auto-build and test on push
4. **Create releases** - Tag versions with release notes

## First Time Contributor Setup

When someone clones and runs for the first time:

```bash
git clone https://github.com/USERNAME/hidden-gems-fbla-2026.git
cd hidden-gems-fbla-2026-main

# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install

# Copy environment template
cp .env.example .env
# Edit .env with their API keys

# Run!
npm run dev
```

Need help? See the main README!
