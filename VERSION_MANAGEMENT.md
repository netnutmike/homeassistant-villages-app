# Version Management

This integration uses semantic versioning (SemVer) to track releases.

## Current Version: 0.1.0

## Version Files

The version is maintained in three places:

### 1. `custom_components/villages_events/__version__.py`
```python
__version__ = "0.1.0"
```
This is the source of truth for the version number.

### 2. `custom_components/villages_events/manifest.json`
```json
{
  "version": "0.1.0"
}
```
Home Assistant reads this to display the version in the UI.

### 3. `custom_components/villages_events/__init__.py`
```python
from .__version__ import __version__
VERSION = __version__
```
Exposes the version for programmatic access.

## Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): New functionality (backwards compatible)
- **PATCH** version (0.0.X): Bug fixes (backwards compatible)

### Examples:
- `0.1.0` → `0.1.1`: Bug fix
- `0.1.0` → `0.2.0`: New feature
- `0.1.0` → `1.0.0`: Breaking change

## How to Update Version

When releasing a new version, update these files:

### Step 1: Update `__version__.py`
```python
__version__ = "0.2.0"  # New version
```

### Step 2: Update `manifest.json`
```json
{
  "version": "0.2.0"
}
```

### Step 3: Update `CHANGELOG.md`
Add a new section for the version:
```markdown
## [0.2.0] - 2024-12-XX

### Added
- New feature description

### Fixed
- Bug fix description
```

### Step 4: Update README badge (optional)
```markdown
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)]
```

### Step 5: Commit and Tag
```bash
git add custom_components/villages_events/__version__.py
git add custom_components/villages_events/manifest.json
git add CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main --tags
```

## Version Display in Home Assistant

After updating the version:

1. **Restart Home Assistant** (full restart required)
2. Go to **Settings** → **Devices & Services**
3. Find "The Villages Events"
4. Click on it to see the integration details
5. The version should be displayed

## HACS Version Display

For HACS to show the correct version:

1. Version must be in `manifest.json`
2. Create a GitHub release with matching tag (e.g., `v0.2.0`)
3. HACS will automatically detect the new version
4. Users will see an update notification

## Creating a GitHub Release

1. Go to your repository on GitHub
2. Click **Releases** → **Create a new release**
3. Tag: `v0.2.0` (must match version)
4. Title: `Version 0.2.0`
5. Description: Copy from CHANGELOG.md
6. Click **Publish release**

## Version History

- **0.1.0** (2024-12-06): Initial release
  - Per-venue event sensors
  - Favorite performer tracking
  - Live API integration
  - Home Assistant events
  - Manual refresh service

## Checking Current Version

### In Python:
```python
from custom_components.villages_events import VERSION
print(VERSION)  # Output: 0.1.0
```

### In Home Assistant:
1. Settings → Devices & Services
2. Click on "The Villages Events"
3. Version shown in integration details

### Via Command Line:
```bash
grep version custom_components/villages_events/manifest.json
```

## Pre-release Versions

For beta/alpha releases, use:
- `0.2.0-beta.1`
- `0.2.0-alpha.1`
- `0.2.0-rc.1`

Update all three version files with the pre-release tag.
