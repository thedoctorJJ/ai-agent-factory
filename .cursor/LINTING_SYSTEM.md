# Linting System - AI Agent Factory

**Status**: ✅ **FULLY OPERATIONAL**  
**Last Updated**: November 27, 2025

---

## 📋 System Overview

The AI Agent Factory now has a comprehensive linting system covering all code types:
- ✅ Python (Black, Flake8, MyPy, isort, Pylint)
- ✅ JavaScript/TypeScript (ESLint, Prettier)
- ✅ Shell Scripts (ShellCheck)
- ✅ Markdown (Markdownlint)
- ✅ Pre-commit hooks (automated)
- ✅ GitHub Actions CI/CD (automated)

---

## 🚀 Quick Start

### Run All Linters
```bash
./scripts/dev/lint-all.sh
```

### Run Individual Linters
```bash
./scripts/dev/lint-python.sh      # Python only
./scripts/dev/lint-frontend.sh    # JavaScript/TypeScript only
./scripts/dev/lint-scripts.sh     # Shell scripts only
./scripts/dev/lint-markdown.sh    # Markdown only
```

### Auto-fix Issues
```bash
# Python
cd backend
python3 -m black fastapi_app/
python3 -m isort fastapi_app/

# Frontend
cd frontend/next-app
npx prettier --write "**/*.{ts,tsx,js,jsx,json,css}"
npx eslint "**/*.{ts,tsx,js,jsx}" --fix

# Markdown
markdownlint "**/*.md" --fix
```

---

## 🛠️ Installed Tools

### Python Linters (5 tools)
1. ✅ **Black** (v25.11.0) - Code formatter
2. ✅ **Flake8** (v7.3.0) - Style guide enforcement
3. ✅ **MyPy** (v1.18.2) - Type checker
4. ✅ **isort** (v7.0.0) - Import sorter
5. ✅ **Pylint** (v4.0.3) - Code quality analyzer

### JavaScript/TypeScript Linters (2 tools)
6. ✅ **ESLint** (v9.39.1) - JavaScript/TypeScript linter
7. ✅ **Prettier** (v3.7.1) - Code formatter

### Shell Linters (1 tool)
8. ✅ **ShellCheck** (v0.11.0) - Shell script analyzer

### Markdown Linters (1 tool)
9. ✅ **Markdownlint** - Markdown linter/formatter

### Other Tools (1 tool)
10. ✅ **Pre-commit** (v4.5.0) - Git hook framework

**Total**: 10/10 tools installed ✅

---

## 📁 Configuration Files

### Python Configuration
- **`pyproject.toml`** - Black, isort, MyPy, Pylint configuration
- **`.flake8`** - Flake8 configuration

### Frontend Configuration
- **`frontend/next-app/.eslintrc.json`** - ESLint rules
- **`frontend/next-app/.prettierrc`** - Prettier formatting options
- **`frontend/next-app/.prettierignore`** - Files to ignore

### Markdown Configuration
- **`.markdownlint.json`** - Markdownlint rules

### Pre-commit Configuration
- **`.pre-commit-config.yaml`** - Pre-commit hooks setup

### GitHub Actions
- **`.github/workflows/lint.yml`** - CI/CD linting workflow

---

## 🔧 Configuration Details

### Python Settings
- **Line length**: 100 characters
- **Python version**: 3.11
- **Profile**: Black-compatible
- **Type checking**: Enabled (non-blocking)

### Frontend Settings
- **Line length**: 100 characters
- **Quote style**: Double quotes
- **Semicolons**: Required
- **Trailing commas**: ES5
- **TypeScript**: Strict mode enabled

### Shell Scripts
- **Follow sources**: Enabled (-x flag)
- **Severity**: All warnings

### Markdown
- **Line length**: Disabled (no max)
- **Heading style**: ATX (#)
- **List style**: Dash (-)
- **HTML**: Allowed

---

## 🎯 Linting Workflow

### During Development
```bash
# Lint as you code (continuous)
# Run relevant linter for the file you're editing

# Python file
python3 -m black path/to/file.py --check
python3 -m flake8 path/to/file.py

# TypeScript file
cd frontend/next-app
npx eslint path/to/file.tsx
npx prettier path/to/file.tsx --check

# Shell script
shellcheck path/to/script.sh

# Markdown file
markdownlint path/to/file.md
```

### Before Commit
```bash
# Run all linters
./scripts/dev/lint-all.sh

# Or let pre-commit hooks do it automatically
git commit -m "..."
# Pre-commit hooks will run automatically
```

### In CI/CD
- GitHub Actions runs on every push/PR
- All 4 linting jobs run in parallel
- Must pass before merge

---

## 🔄 Pre-commit Hooks

### What They Do
Pre-commit hooks run automatically before every git commit:
1. **Black** - Auto-format Python code
2. **isort** - Sort Python imports
3. **Flake8** - Check Python style
4. **Prettier** - Format JS/TS/JSON/CSS/YAML
5. **ShellCheck** - Lint shell scripts
6. **Markdownlint** - Lint and fix Markdown
7. **General checks** - Trailing whitespace, large files, private keys, etc.

### Installation
Already installed! Pre-commit hooks are active in this repository.

### Skip Hooks (when needed)
```bash
# Skip pre-commit hooks (use sparingly!)
git commit --no-verify -m "message"
```

### Update Hooks
```bash
pre-commit autoupdate
```

---

## 🤖 GitHub Actions Workflow

### Jobs
1. **python-lint** - Black, isort, Flake8, MyPy
2. **frontend-lint** - Prettier, ESLint, TypeScript
3. **shell-lint** - ShellCheck
4. **markdown-lint** - Markdownlint

### Triggers
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### Status
All jobs must pass ✅ for PR approval

---

## 📚 For AI Agents

### When to Lint

**Always**:
- ✅ During development (lint as you code)
- ✅ Before committing (run lint-all.sh)
- ✅ After making any code changes

**Workflow**:
```
1. Make code changes
   ↓
2. Lint relevant files
   ↓
3. Fix any issues
   ↓
4. Run full lint check (./scripts/dev/lint-all.sh)
   ↓
5. Commit (pre-commit hooks run automatically)
```

### Common Commands

**Check single file**:
```bash
# Python
python3 -m black file.py --check
python3 -m flake8 file.py

# TypeScript
cd frontend/next-app && npx eslint file.tsx

# Shell
shellcheck script.sh

# Markdown
markdownlint file.md
```

**Auto-fix single file**:
```bash
# Python
python3 -m black file.py
python3 -m isort file.py

# TypeScript
cd frontend/next-app && npx prettier file.tsx --write
cd frontend/next-app && npx eslint file.tsx --fix

# Markdown
markdownlint file.md --fix
```

**Check all files**:
```bash
./scripts/dev/lint-all.sh
```

### Integration with Workflow

Linting is **Phase 3** (Quality Assurance) in the AI Agent Workflow:

```
Phase 1: Session Startup
Phase 2: Problem Solving (lint during!)
Phase 3: Quality Assurance
  ├─ Run ./scripts/dev/lint-all.sh  ← HERE
  ├─ Fix any issues
  └─ Verify all passed
Phase 4: Documentation
Phase 5: Git Commit (pre-commit hooks run automatically)
Phase 6: Session Closure
```

---

## ⚠️ Troubleshooting

### Python linters not found
```bash
pip3 install black flake8 mypy isort pylint
```

### ESLint/Prettier not found
```bash
cd frontend/next-app
npm install
```

### ShellCheck not found
```bash
brew install shellcheck
```

### Markdownlint not found
```bash
npm install -g markdownlint-cli
```

### Pre-commit not working
```bash
pip3 install pre-commit
cd /path/to/repo
pre-commit install
```

---

## 📊 Linting Standards

### Python
- **Max line length**: 100
- **Style**: Black + Flake8
- **Imports**: Sorted with isort
- **Types**: MyPy type hints (recommended)
- **Quality**: Pylint score > 8.0

### JavaScript/TypeScript
- **Max line length**: 100
- **Style**: Prettier + ESLint
- **Types**: TypeScript strict mode
- **React**: Hooks rules enforced
- **Warnings**: Zero warnings policy

### Shell Scripts
- **Style**: POSIX-compliant where possible
- **Quoting**: Always quote variables
- **Error handling**: `set -e` for safety
- **Functions**: Use snake_case

### Markdown
- **Headings**: ATX style (#)
- **Lists**: Dash (-) style
- **Line length**: No limit
- **HTML**: Allowed where needed

---

## 🎯 Quick Reference

| File Type | Linter | Config File | Script |
|-----------|--------|-------------|--------|
| Python | Black, Flake8, MyPy, isort | `pyproject.toml`, `.flake8` | `lint-python.sh` |
| TypeScript | ESLint, Prettier | `.eslintrc.json`, `.prettierrc` | `lint-frontend.sh` |
| Shell | ShellCheck | None | `lint-scripts.sh` |
| Markdown | Markdownlint | `.markdownlint.json` | `lint-markdown.sh` |
| All | All tools | All configs | `lint-all.sh` |

---

## ✅ Success Criteria

Linting passes when:
- ✅ All Python files formatted with Black
- ✅ All Python imports sorted with isort
- ✅ No Flake8 violations
- ✅ No MyPy errors (type hints correct)
- ✅ All TypeScript/JavaScript formatted with Prettier
- ✅ No ESLint errors or warnings
- ✅ No TypeScript type errors
- ✅ All shell scripts pass ShellCheck
- ✅ All Markdown files pass markdownlint

**Current Status**: ✅ **FULLY OPERATIONAL**

---

## 🔗 Related Files

- **Workflow**: `docs/guides/AI_AGENT_WORKFLOW.md`
- **Quick Reference**: `.cursor/QUICK_REFERENCE.md`
- **Startup Prompt**: `.cursor/startup-prompt.md`
- **Scripts**: `scripts/dev/lint-*.sh`
- **GitHub Actions**: `.github/workflows/lint.yml`

---

**Last Updated**: November 27, 2025  
**Version**: 2.0  
**Status**: ✅ Active and fully operational

**Remember**: Lint during development, not just before commit!
