# 🔍 SonarQube Setup Guide

## What is SonarQube?

SonarQube analyzes code quality, detects bugs, security vulnerabilities, and code smells.

Your repo has a **required status check** for "SonarQube Code Analysis" on the main branch.

---

## Option 1: Use Company SonarQube Server (Recommended)

### Prerequisites
Ask your DevOps/IT team for:
1. **SonarQube Server URL** (e.g., `https://sonarqube.dealertrack.com`)
2. **Project Token** (for authentication)
3. **Project Key** (if pre-created)

### Setup GitHub Secrets

1. Go to: https://github.com/tdr-dealertrack/qa-testing-garage/settings/secrets/actions
2. Click **New repository secret**
3. Add these secrets:
   - **Name:** `SONAR_TOKEN`  
     **Value:** `<your-sonarqube-token>`
   - **Name:** `SONAR_HOST_URL`  
     **Value:** `<your-sonarqube-server-url>`

### Verify
- Push to `develop` branch
- Check GitHub Actions: `.github/workflows/sonarqube.yml` runs
- SonarQube dashboard shows analysis

---

## Option 2: Use SonarCloud (Free for Public Repos)

### Setup

1. Go to: https://sonarcloud.io
2. Sign in with GitHub
3. Click **Analyze new project**
4. Select `tdr-dealertrack/qa-testing-garage`
5. Get your token

### Configure

1. Update `.sonarcloud.properties`:
   ```properties
   sonar.organization=YOUR_ORG_KEY
   ```

2. Add GitHub secret:
   - **Name:** `SONAR_TOKEN`
   - **Value:** `<sonarcloud-token>`

3. No `SONAR_HOST_URL` needed (SonarCloud default)

---

## Option 3: Temporary - Disable for Hackathon

**For rapid development during hackathon:**

### Disable Branch Protection (Temporarily)

1. Go to: https://github.com/tdr-dealertrack/qa-testing-garage/settings/branches
2. Click **Edit** on the `main` branch rule
3. **Uncheck:** "Require status checks to pass before merging"
4. Or remove "SonarQube Code Analysis" from required checks
5. Save changes

**Important:** Re-enable after hackathon!

---

## Configuration Files

We've created:

1. **`sonar-project.properties`**
   - Main SonarQube config
   - Defines what to scan
   - Exclusions for node_modules, tests, etc.

2. **`.github/workflows/sonarqube.yml`**
   - GitHub Action to run analysis
   - Runs on push to main/develop
   - Includes test coverage

3. **`.sonarcloud.properties`**
   - Alternative config for SonarCloud
   - Use if company doesn't have self-hosted SonarQube

---

## Running Locally (Optional)

### With Docker:

```bash
# Start SonarQube locally
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Wait for startup (2-3 minutes)
# Open: http://localhost:9000
# Default login: admin/admin

# Generate token in SonarQube UI
# Run scanner:
docker run --rm \
  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
  -e SONAR_TOKEN="your-token" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

---

## What Gets Analyzed

### Python Backend:
- Code quality issues
- Security vulnerabilities
- Code coverage (from pytest)
- Complexity metrics
- Duplicate code

### React Frontend:
- JavaScript/TypeScript issues
- Code smells
- Best practices
- Potential bugs

### Exclusions (Don't Scan):
- `node_modules/`
- `__pycache__/`
- Test files
- Docker configs
- Build artifacts

---

## Quality Metrics

SonarQube will report:

| Metric | Description |
|--------|-------------|
| **Bugs** | Actual code errors |
| **Vulnerabilities** | Security issues |
| **Code Smells** | Maintainability issues |
| **Coverage** | Test coverage % |
| **Duplications** | Duplicate code blocks |
| **Complexity** | Cyclomatic complexity |

---

## Fixing Issues

### View Results:
1. Go to SonarQube dashboard
2. Click on project
3. See issues by severity

### Common Fixes:

**Python:**
- Use ruff to auto-fix: `poetry run ruff check --fix .`
- Run tests: `poetry run pytest`

**JavaScript:**
- Run linter: `npm run lint`
- Fix auto-fixable: `npm run lint -- --fix`

---

## CI/CD Integration

The workflow (`.github/workflows/sonarqube.yml`):

1. **Triggers:** Push to main/develop, or PR
2. **Runs tests:** Generates coverage reports
3. **Scans code:** Sends to SonarQube
4. **Quality Gate:** Checks if code meets standards
5. **Status:** Reports pass/fail to GitHub

**Note:** `continue-on-error: true` means it won't block PRs during hackathon

---

## Troubleshooting

### "SONAR_TOKEN not found"
- Add secret in GitHub repo settings
- Check spelling: `SONAR_TOKEN` (all caps)

### "Quality Gate failed"
- Review issues in SonarQube dashboard
- For hackathon: Set `continue-on-error: true` in workflow
- Or ask admin to adjust Quality Gate thresholds

### "Shallow clones should be disabled"
- Already fixed in workflow: `fetch-depth: 0`

### Analysis not appearing
- Check GitHub Actions logs
- Verify SONAR_HOST_URL is correct
- Confirm project key matches

---

## For Hackathon

**Quick Solution:**
1. Ask DevOps for SONAR_TOKEN and SONAR_HOST_URL
2. Add as GitHub secrets
3. Push to develop → SonarQube runs automatically

**OR**

Temporarily disable branch protection (Option 3 above)

---

## After Hackathon

1. Review SonarQube findings
2. Fix critical/high severity issues
3. Improve test coverage
4. Re-enable branch protection
5. Make SonarQube Quality Gate required

---

**Need help?** Ask your DevOps team for SonarQube credentials!
