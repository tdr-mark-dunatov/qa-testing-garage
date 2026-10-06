# ⚠️ IMPORTANT - Use `develop` Branch!

## For Team Members

**All hackathon work is on the `develop` branch, NOT `main`.**

### Clone & Setup

```bash
git clone https://github.com/tdr-dealertrack/qa-testing-garage.git
cd qa-testing-garage

# ⚠️ IMPORTANT: Switch to develop branch
git checkout develop

# Now follow DEV_SETUP.md
```

### Why `develop` and not `main`?

The `main` branch has a SonarQube requirement that blocks merges.  
For hackathon speed, we're working on `develop` branch.

**After hackathon:** We'll merge `develop` → `main` with proper code analysis.

---

## Current Branch Status

- **`develop`** ← ✅ Use this! Has all latest code (PostgreSQL, tests, docs, SonarQube config)
- **`main`** ← ❌ Old, blocked by branch protection

---

## Team Workflow

```bash
# 1. Make sure you're on develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/pii-detection

# 3. Make changes, commit
git add .
git commit -m "Add PII detection module"

# 4. Push your branch
git push origin feature/pii-detection

# 5. Create PR to `develop` (not main!)
```

---

**TL;DR: Use `develop` branch for everything!**
