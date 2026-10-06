# Poetry Migration Complete! 🎉

## What Changed

We've migrated from `pip` + `requirements.txt` to **Poetry** for Python dependency management.

## Why Poetry?

✅ Better dependency resolution  
✅ Automatic virtual environment management  
✅ Lock file for reproducible builds  
✅ Separation of dev and production dependencies  
✅ Modern Python packaging standard  

## Files Updated

### Added:
- ✅ `apps/api/pyproject.toml` - Poetry configuration
- ✅ `apps/api/README.md` - API documentation
- ✅ `DEPLOYMENT.md` - Deployment guide

### Modified:
- ✅ `apps/api/Dockerfile` - Now uses Poetry
- ✅ `scripts/dev.sh` - Unix dev script uses Poetry
- ✅ `scripts/dev.bat` - Windows dev script uses Poetry
- ✅ `package.json` - Root scripts use Poetry
- ✅ `README.md` - Updated instructions
- ✅ `apps/web/src/App.jsx` - Fixed WebSocket for HTTPS (wss://)
- ✅ `apps/api/main.py` - Production-ready CORS with env vars

### Removed:
- ❌ `apps/api/requirements.txt` - Replaced by pyproject.toml

## Quick Start

### First Time Setup:

**1. Install Poetry (if not installed):**
```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Mac/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Or via pip
pip install poetry
```

**2. Install Dependencies:**
```bash
cd apps/api
poetry install
```

This will:
- Create a virtual environment automatically
- Install all dependencies
- Generate `poetry.lock` file (commit this!)

### Development:

**Option 1: Quick Dev Scripts**
```bash
# Windows
scripts\dev.bat

# Mac/Linux
./scripts/dev.sh
```

**Option 2: Manual**
```bash
# Terminal 1 - API
cd apps/api
poetry run uvicorn main:app --reload

# Terminal 2 - Web
cd apps/web
npm install
npm run dev
```

**Option 3: Docker (No Poetry needed locally!)**
```bash
cd docker
docker-compose up --build
```

## Adding Dependencies

### Production Dependency:
```bash
cd apps/api
poetry add fastapi
```

### Dev Dependency:
```bash
poetry add --group dev pytest
```

### Update All:
```bash
poetry update
```

## Deployment

**Docker handles everything!** The Dockerfile installs Poetry and runs `poetry install` automatically.

No changes needed for:
- ✅ Railway.app
- ✅ Render.com
- ✅ DigitalOcean
- ✅ Any Docker-based deployment

## Backwards Compatibility

If you need a `requirements.txt` for legacy systems:

```bash
cd apps/api
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

## Commands Cheat Sheet

```bash
# Install dependencies
poetry install

# Run command in Poetry env
poetry run uvicorn main:app --reload

# Activate Poetry shell (then run commands normally)
poetry shell
uvicorn main:app --reload

# Add dependency
poetry add package-name

# Remove dependency
poetry remove package-name

# Update dependencies
poetry update

# Show installed packages
poetry show

# Check for issues
poetry check
```

## Troubleshooting

### "poetry: command not found"
Install Poetry first (see "Install Poetry" above)

### "poetry.lock" doesn't exist
Run `poetry install` - it will be created automatically

### Virtual environment location
```bash
poetry env info  # Shows venv path
poetry env list  # Lists all venvs
```

### Clear cache
```bash
poetry cache clear pypi --all
```

## Next Steps

1. ✅ Run `poetry install` in `apps/api`
2. ✅ Test locally with `scripts/dev.bat` or `scripts/dev.sh`
3. ✅ Test with Docker: `cd docker && docker-compose up --build`
4. ✅ Deploy to Railway/Render/DigitalOcean
5. ✅ Commit `poetry.lock` to Git

---

🎉 **Poetry migration complete! Your Python dependency management is now modern and robust.**
